"""Build twice in an isolated copy; require every shipped byte to reproduce."""
from pathlib import Path
import hashlib
import shutil
import subprocess
import sys
import tempfile

root = Path(__file__).resolve().parents[2]
def hashes(folder):
    return {p.relative_to(folder).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in folder.rglob('*') if p.is_file()}

expected = hashes(root / 'docs')
qa_root = (root/'redesign/qa-output').resolve()
qa_root.mkdir(parents=True, exist_ok=True)
with tempfile.TemporaryDirectory(prefix='generator-', dir=qa_root) as temp:
    assert Path(temp).resolve().is_relative_to(qa_root), 'Temporary build must remain inside QA workspace'
    target = Path(temp) / 'docs'
    shutil.copytree(root / 'docs', target)
    for attempt in (1, 2):
        subprocess.run([sys.executable, '-B', str(root/'site-source/_src/build.py'),
                        '--out', str(target)], check=True, capture_output=True)
        actual = hashes(target)
        changed = sorted(k for k in expected.keys() | actual.keys()
                         if expected.get(k) != actual.get(k))
        assert not changed, (attempt, changed)
assert hashes(root/'docs') == expected, 'Original docs changed during isolated builds'
for p in list((root/'site-source').rglob('*.py')) + list((root/'redesign/qa').glob('*.py')):
    compile(p.read_text(encoding='utf-8'), str(p), 'exec')
print(f'PASS: two isolated generator builds reproduce all {len(expected)} docs files; '
      'assets and live scripts preserved; all generator/QA Python syntax valid.')
