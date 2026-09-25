"""배포에 필요한 두 Python 파일만 별도 폴더에 준비합니다."""

from pathlib import Path
from shutil import copyfile

ROOT = Path(__file__).resolve().parent.parent
DESTINATION = ROOT / ".wrangler" / "city-fit"


def build():
    if not (ROOT / "python_modules" / "workers" / "__init__.py").is_file():
        raise SystemExit("Cloudflare SDK is missing. Run: npm run setup:cloudflare")
    DESTINATION.mkdir(parents=True, exist_ok=True)
    for filename in ("worker.py", "quiz.py"):
        copyfile(ROOT / "src" / filename, DESTINATION / filename)


if __name__ == "__main__":
    build()
