#!/usr/bin/env python3
"""Isolated memory roundtrip with explicit demo opt-in, no lasting user storage."""
import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SCRIPT=ROOT/'.agents/skills/auto-validate/scripts/auto_validate.py'
AUDIT=ROOT/'examples/cases/ui/audit-before.json'

def main():
    with tempfile.TemporaryDirectory(prefix='auto-validate-memory-demo-') as directory:
        memory=Path(directory)/'rules.jsonl'
        report=Path(directory)/'report.md'
        assert not memory.exists(), 'demo should begin empty'
        subprocess.run([sys.executable,str(SCRIPT),'check','--input',str(AUDIT),'--output',str(report),'--save-memory','--memory-path',str(memory)],check=True,capture_output=True,text=True)
        saved=[json.loads(line) for line in memory.read_text(encoding='utf-8').splitlines() if line.strip()]
        search=subprocess.run([sys.executable,str(SCRIPT),'memory','search','--path',str(memory),'--project','demo-ui','--query','seções solicitadas'],check=True,capture_output=True,text=True)
        found=json.loads(search.stdout)
        assert len(saved)==len(found)==1, (len(saved),len(found))
        print('MEMÓRIA — exemplo isolado (opt-in apenas para teste)')
        print('Antes: 0 regras | Após opt-in de demonstração: 1 regra | Recuperadas: 1 regra')
        print('Regra:',found[0]['rule'])
    print('O armazenamento temporário foi descartado; não foi criada memória do usuário.')

if __name__=='__main__': main()
