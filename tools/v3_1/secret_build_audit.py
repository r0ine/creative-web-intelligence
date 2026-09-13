"""Defensive heuristic audit for accidental secrets in text-based frontend/build output.
Usage: python tools/v3_1/secret_build_audit.py <directory>
This is a guardrail, not proof that a project is secure.
"""
from pathlib import Path
import re, sys
root=Path(sys.argv[1] if len(sys.argv)>1 else '.')
patterns=[
 ('private-key', re.compile(r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----')),
 ('github-token-like', re.compile(r'\b(?:ghp|github_pat)_[A-Za-z0-9_]{20,}\b')),
 ('anthropic-key-like', re.compile(r'\bsk-ant-[A-Za-z0-9_-]{20,}\b')),
 ('generic-secret-assignment', re.compile(r'(?i)\b(?:api[_-]?key|client[_-]?secret|webhook[_-]?secret|session[_-]?secret|password)\s*[:=]\s*["\'][^"\']{12,}["\']')),
]
exts={'.js','.mjs','.cjs','.ts','.tsx','.jsx','.html','.json','.map','.css','.env','.txt','.md','.yml','.yaml'}
findings=[]
for p in root.rglob('*'):
    if not p.is_file() or p.suffix.lower() not in exts or p.stat().st_size>5_000_000: continue
    try: text=p.read_text(encoding='utf-8',errors='ignore')
    except Exception: continue
    for name,rx in patterns:
        if rx.search(text): findings.append((name,str(p)))
if findings:
    print('Potential secret exposure patterns found:')
    for n,p in findings: print(f'- {n}: {p}')
    sys.exit(2)
print('No configured secret patterns found. This does NOT prove absence of secrets.')
