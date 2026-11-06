#!/usr/bin/env python3
"""Auto-Validate: evidence-backed audit scoring and opt-in JSONL memory.

This program does not assess semantic correctness or invoke any LLM.
Python 3.10+; no external dependencies.
"""
import argparse
import json
import os
import re
import sys
import tempfile
import uuid
from datetime import datetime, timezone
from pathlib import Path

WEIGHTS = {"fidelity": 0.35, "completeness": 0.25, "accuracy": 0.20,
           "constraints": 0.15, "usability": 0.05}
REQUIREMENT_TYPES = {"must", "must_not", "should"}
STATUSES = {"met", "partial", "missed", "violated", "unverifiable"}
SEVERITIES = {"critical", "major", "minor"}
CLASSIFICATIONS = {"observed", "hypothesis"}
STOP = set("a o as os um uma de do da dos das em no na nos nas para por com sem que e ou the and of for in to is on by this that".split())


class AuditError(ValueError):
    pass


def read_json(path):
    try:
        data = json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise AuditError(f"Não foi possível ler JSON {path}: {exc}") from exc
    if not isinstance(data, dict):
        raise AuditError("O JSON deve conter um objeto na raiz.")
    return data


def required_str(obj, key, where):
    val = obj.get(key)
    if not isinstance(val, str) or not val.strip():
        raise AuditError(f"{where}.{key} deve ser texto não vazio.")
    return val.strip()


def validate(data):
    if data.get("schema_version") != "1.0":
        raise AuditError("schema_version deve ser '1.0'.")
    for key in ("project", "request", "deliverable", "scope"):
        required_str(data, key, "audit")
    criteria = data.get("criteria")
    if not isinstance(criteria, dict) or set(criteria) != set(WEIGHTS):
        raise AuditError(f"criteria deve conter exatamente: {', '.join(WEIGHTS)}")
    for key, value in criteria.items():
        if isinstance(value, bool) or not isinstance(value, (int, float)) or not 0 <= value <= 10:
            raise AuditError(f"criteria.{key} deve ser número entre 0 e 10.")
    requirements = data.get("requirements")
    if not isinstance(requirements, list) or not requirements:
        raise AuditError("requirements deve ser uma lista não vazia.")
    rids = set()
    for i, req in enumerate(requirements):
        if not isinstance(req, dict):
            raise AuditError(f"requirements[{i}] deve ser objeto.")
        where = f"requirements[{i}]"
        rid = required_str(req, "id", where)
        for key in ("text", "evidence"):
            required_str(req, key, where)
        if rid in rids:
            raise AuditError(f"ID de requisito duplicado: {rid}")
        rids.add(rid)
        if req.get("type") not in REQUIREMENT_TYPES:
            raise AuditError(f"{where}.type inválido.")
        if req.get("status") not in STATUSES:
            raise AuditError(f"{where}.status inválido.")
    findings = data.get("findings")
    if not isinstance(findings, list):
        raise AuditError("findings deve ser uma lista (pode estar vazia).")
    fids = set()
    findings_by_req = set()
    for i, finding in enumerate(findings):
        if not isinstance(finding, dict):
            raise AuditError(f"findings[{i}] deve ser objeto.")
        where = f"findings[{i}]"
        fid = required_str(finding, "id", where)
        if fid in fids:
            raise AuditError(f"ID de finding duplicado: {fid}")
        fids.add(fid)
        rid = required_str(finding, "requirement_id", where)
        if rid not in rids:
            raise AuditError(f"Finding {fid} refere requisito inexistente: {rid}")
        for key in ("expected", "observed", "evidence", "fix", "verify"):
            required_str(finding, key, where)
        if finding.get("severity") not in SEVERITIES:
            raise AuditError(f"{where}.severity inválida.")
        if finding.get("classification") not in CLASSIFICATIONS:
            raise AuditError(f"{where}.classification inválida.")
        if finding["classification"] == "observed":
            findings_by_req.add(rid)
    for req in requirements:
        if req["status"] in ("partial", "missed", "violated") and req["id"] not in findings_by_req:
            raise AuditError(f"Requisito {req['id']} tem desvio, mas não há finding observado correspondente.")
    candidates = data.get("memory_candidates", [])
    if not isinstance(candidates, list):
        raise AuditError("memory_candidates deve ser uma lista.")
    observed_fids = {f["id"] for f in findings if f["classification"] == "observed"}
    for i, candidate in enumerate(candidates):
        if not isinstance(candidate, dict):
            raise AuditError(f"memory_candidates[{i}] deve ser objeto.")
        for key in ("rule", "reason", "source_finding_id"):
            required_str(candidate, key, f"memory_candidates[{i}]")
        if candidate.get("scope") not in ("project", "global"):
            raise AuditError(f"memory_candidates[{i}].scope deve ser project ou global.")
        if candidate["source_finding_id"] not in observed_fids:
            raise AuditError(f"Memória candidata {i}: referência deve ser a finding observado.")
    return data


def score(data):
    raw = round(sum(data["criteria"][k] * WEIGHTS[k] for k in WEIGHTS) + 1e-9, 1)
    final = raw
    caps = []
    reqs = data["requirements"]
    if any(r["type"] == "must_not" and r["status"] == "violated" for r in reqs):
        caps.append((3.0, "Restrição expressa violada (must_not)."))
    if any(r["type"] == "must" and r["status"] in {"missed", "violated"} for r in reqs):
        caps.append((6.0, "Requisito obrigatório descumprido (must)."))
    observed = [f for f in data["findings"] if f["classification"] == "observed"]
    if any(f["severity"] == "critical" for f in observed):
        caps.append((3.0, "Desvio crítico observado."))
    if any(f["severity"] == "major" for f in observed):
        caps.append((7.0, "Desvio importante observado."))
    if any(r["type"] == "must" and r["status"] == "unverifiable" for r in reqs):
        caps.append((8.0, "Requisito obrigatório não verificável."))
    for cap, _ in caps:
        final = min(final, cap)
    return {"raw": raw, "final": final, "caps": [reason for cap, reason in caps if cap < raw]}


def escape_md(value):
    return str(value).replace("|", "\\|").replace("\n", " ").strip()


def report(data):
    s = score(data)
    lines = ["# Auto-Validate — Relatório de avaliação", "",
             f"**Projeto:** {data['project']}", f"**Entrega:** {data['deliverable']}",
             f"**Escopo:** {data['scope']}", "",
             f"## Nota geral: {s['final']:.1f}/10", "",
             f"**Média ponderada:** {s['raw']:.1f}/10", "",
             "| Critério | Nota | Peso |", "|---|---:|---:|"]
    for key, weight in WEIGHTS.items():
        lines.append(f"| {key} | {data['criteria'][key]:g}/10 | {weight:.0%} |")
    if s["caps"]:
        lines.extend(["", "**Limites aplicados:** " + "; ".join(s["caps"])])
    lines.extend(["", "## Requisitos auditados", "", "| ID | Tipo | Status | Requisito | Evidência |",
                  "|---|---|---|---|---|"])
    for r in data["requirements"]:
        lines.append("| " + " | ".join(escape_md(r[k]) for k in ("id", "type", "status", "text", "evidence")) + " |")
    lines.extend(["", "## Desvios e correções", ""])
    if not data["findings"]:
        lines.append("Nenhum desvio foi registrado dentro do escopo inspecionado.")
    for finding in data["findings"]:
        lines.extend([f"### {finding['id']} — {finding['requirement_id']} ({finding['severity']}, {finding['classification']})", "",
                      f"- **Esperado:** {finding['expected']}",
                      f"- **Observado:** {finding['observed']}",
                      f"- **Evidência:** {finding['evidence']}",
                      f"- **Correção proposta:** {finding['fix']}",
                      f"- **Como validar:** {finding['verify']}"])
        if finding.get("possible_cause"):
            lines.append(f"- **Causa possível (hipótese):** {finding['possible_cause']}")
        lines.append("")
    lines.extend(["## Memória", "", "Candidatas à memória (não salvas automaticamente):"])
    if not data.get("memory_candidates"):
        lines.append("- Nenhuma")
    for c in data.get("memory_candidates", []):
        lines.append(f"- [{c['scope']}] {c['rule']} (origem: {c['source_finding_id']})")
    lines.extend(["", "## Limitações", "", "A nota usa critérios fornecidos pelo agente. Este script verifica consistência e calcula notas, mas não verifica semanticamente a verdade das evidências."])
    if data.get("notes"):
        lines.extend(["", f"**Observações:** {data['notes']}"])
    return "\n".join(lines) + "\n"


def read_memory(path):
    file = Path(path)
    if not file.exists():
        return []
    rows = []
    index = 0
    try:
        for index, line in enumerate(file.read_text(encoding="utf-8").splitlines(), start=1):
            if not line.strip():
                continue
            obj = json.loads(line)
            if not isinstance(obj, dict) or not obj.get("id") or not obj.get("rule"):
                raise ValueError("registro inválido")
            rows.append(obj)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        raise AuditError(f"Memória malformada em {file}, linha {index}: {exc}") from exc
    return rows


def write_memory(path, rows):
    dest = Path(path)
    dest.parent.mkdir(parents=True, exist_ok=True)
    name = None
    try:
        with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=dest.parent, prefix=".auto-validate-", delete=False) as handle:
            name = handle.name
            for row in rows:
                handle.write(json.dumps(row, ensure_ascii=False) + "\n")
        os.replace(name, dest)
    finally:
        if name and os.path.exists(name):
            os.unlink(name)


def normalize(text):
    return " ".join(str(text).casefold().split())


def save_learning(path, data):
    items = read_memory(path)
    signatures = {(item.get("scope"), item.get("project"), normalize(item["rule"])) for item in items}
    added = 0
    for c in data.get("memory_candidates", []):
        project = data["project"] if c["scope"] == "project" else "*"
        signature = (c["scope"], project, normalize(c["rule"]))
        if signature in signatures:
            continue
        items.append({"id": uuid.uuid4().hex[:12], "created_at": datetime.now(timezone.utc).isoformat(),
                      "project": project, "scope": c["scope"], "rule": c["rule"],
                      "reason": c["reason"], "source_finding_id": c["source_finding_id"]})
        signatures.add(signature)
        added += 1
    if added:
        write_memory(path, items)
    return added


def words(text):
    return {w for w in re.findall(r"[^\W_]+", text.casefold()) if len(w) >= 3 and w not in STOP}


def search_memory(items, query, project):
    tokens = words(query)
    if not tokens:
        raise AuditError("A consulta precisa conter pelo menos uma palavra informativa.")
    scored = []
    for item in items:
        if item.get("scope") == "project" and item.get("project") != project:
            continue
        hits = len(tokens & words(item["rule"] + " " + item.get("reason", "")))
        if hits:
            scored.append((hits, item))
    return [item for _, item in sorted(scored, key=lambda v: -v[0])]


def build_parser():
    p = argparse.ArgumentParser(description="Auditoria 0–10 e memória persistente opt-in.")
    sub = p.add_subparsers(dest="command", required=True)
    check = sub.add_parser("check", help="Validar uma avaliação, pontuar e gerar relatório.")
    check.add_argument("--input", required=True)
    check.add_argument("--output", help="Caminho do relatório Markdown; imprime em stdout se omitido.")
    check.add_argument("--json-out", help="Resumo da nota em JSON.")
    check.add_argument("--save-memory", action="store_true", help="Autoriza persistir candidatas após revisão.")
    check.add_argument("--memory-path", help="Caminho persistente do JSONL (obrigatório com --save-memory).")
    memory = sub.add_parser("memory", help="Inspecionar, pesquisar ou remover regras salvas.")
    actions = memory.add_subparsers(dest="action", required=True)
    for action in ("list", "search", "remove"):
        a = actions.add_parser(action)
        a.add_argument("--path", required=True)
        if action == "search":
            a.add_argument("--query", required=True)
            a.add_argument("--project", default="")
        elif action == "remove":
            a.add_argument("--id", required=True)
    return p


def main(argv=None):
    args = build_parser().parse_args(argv)
    try:
        if args.command == "check":
            if args.save_memory and not args.memory_path:
                raise AuditError("--save-memory exige --memory-path explícito.")
            data = validate(read_json(args.input))
            output = report(data)
            if args.output:
                target = Path(args.output)
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text(output, encoding="utf-8")
                print(f"Relatório: {target}")
            else:
                print(output)
            result = score(data)
            print(f"Nota: {result['final']:.1f}/10 (média {result['raw']:.1f}/10)", file=sys.stderr)
            if args.json_out:
                json_target = Path(args.json_out)
                json_target.parent.mkdir(parents=True, exist_ok=True)
                json_target.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            if args.save_memory:
                added = save_learning(args.memory_path, data)
                print(f"Memória: {added} regra(s) nova(s) em {args.memory_path}", file=sys.stderr)
        else:
            rows = read_memory(args.path)
            if args.action == "list":
                selected = rows
            elif args.action == "search":
                selected = search_memory(rows, args.query, args.project)
            else:
                selected = [r for r in rows if r["id"] != args.id]
                if len(selected) == len(rows):
                    raise AuditError(f"Regra de memória não encontrada: {args.id}")
                write_memory(args.path, selected)
                print(f"Regra {args.id} removida de {args.path}")
                return 0
            print(json.dumps(selected, ensure_ascii=False, indent=2))
        return 0
    except AuditError as exc:
        print(f"Erro: {exc}", file=sys.stderr)
        return 2
    except OSError as exc:
        print(f"Erro de arquivo: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
