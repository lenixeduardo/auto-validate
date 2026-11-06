#!/usr/bin/env python3
"""Instala o Auto-Validate em um repositório local, sem dependências."""
import argparse
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCE = HERE / ".agents" / "skills" / "auto-validate"


def main():
    parser = argparse.ArgumentParser(description="Instale a skill Auto-Validate em outro repositório.")
    parser.add_argument("repository", help="Caminho do repositório Git de destino (diretório existente).")
    parser.add_argument("--target", choices=("agents", "github"), default="agents",
                        help="'agents' usa .agents/skills; 'github' usa .github/skills.")
    parser.add_argument("--overwrite", action="store_true", help="Substituir skill já instalada.")
    args = parser.parse_args()
    repo = Path(args.repository).expanduser().resolve()
    if not repo.is_dir():
        parser.error(f"Repositório não existe: {repo}")
    folder = ".agents" if args.target == "agents" else ".github"
    destination = repo / folder / "skills" / "auto-validate"
    if destination.exists() and not args.overwrite:
        parser.error(f"Skill já existe: {destination} (use --overwrite para substituir)")
    if destination.resolve() == SOURCE.resolve():
        parser.error("O destino é a instalação de origem.")
    if destination.exists():
        shutil.rmtree(destination)
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(SOURCE, destination)
    print(f"Skill instalada em: {destination}")


if __name__ == "__main__":
    main()
