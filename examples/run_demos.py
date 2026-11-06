#!/usr/bin/env python3
"""Run reproducible Auto-Validate audits on three versioned local examples."""
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / '.agents/skills/auto-validate/scripts/auto_validate.py'
RESULTS = ROOT / 'examples' / 'results'

def main():
    RESULTS.mkdir(parents=True,exist_ok=True)
    for case in ('ui', 'code', 'text'):
        scores = []
        for stage in ('before','after'):
            source = ROOT / 'examples' / 'cases' / case / f'audit-{stage}.json'
            report = RESULTS / f'{case}-{stage}.md'
            result = RESULTS / f'{case}-{stage}.json'
            subprocess.run([sys.executable, str(SCRIPT),'check','--input',str(source),'--output',str(report),'--json-out',str(result)],check=True)
            scores.append(json.loads(result.read_text(encoding='utf8'))['final'])
        assert scores[1] > scores[0], (case, scores)
        print(f'{case:<7} {scores[0]:.1f}/10 -> {scores[1]:.1f}/10 (relatórios: examples/results/)')
    print('Nenhuma memória foi gravada: demonstração sem --save-memory.')

if __name__ == '__main__': main()
