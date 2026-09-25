# Cloudflare 배포 구성

공개 주소: https://assignment01.dojin9512.workers.dev

Cloudflare Worker 이름은 `assignment01`입니다. 화면 파일은 Workers Static Assets가 제공하며, `/api/*` 요청은 `worker.py`에서 처리합니다. 점수 계산은 로컬 앱과 동일한 `quiz.py`를 사용합니다.

## 배포 도구 준비

Node.js 22 이상, Python 3.12 이상과 pip가 필요합니다. Wrangler 버전은 `package-lock.json`, Python Workers SDK 버전은 `requirements-cloudflare.txt`에 고정되어 있습니다.

```bash
npm ci
npm run setup:cloudflare
npx wrangler login
```

`setup:cloudflare`는 공식 `workers-runtime-sdk`의 순수 Python 패키지를 `python_modules/`에 설치합니다. 이 프로젝트는 추가 Python 라이브러리가 없으므로 SDK만 포함하여 Wrangler로 배포합니다. Windows에서 Pywrangler의 Pyodide 가상환경 생성이 실패하는 문제를 피할 수 있습니다.

## 검증과 배포

```bash
npm run deploy:check
npm run dev:cloudflare
```

별도 터미널에서 실행 중인 로컬 Worker를 확인합니다.

```bash
python verify_deployment.py http://localhost:8787
```

공개 배포와 확인:

```bash
npm run deploy
python verify_deployment.py https://assignment01.dojin9512.workers.dev
```

`build_worker.py`는 `worker.py`와 `quiz.py`만 `.wrangler/city-fit/`에 복사합니다. 배포 SDK, 가상환경, `node_modules/`, 빌드 결과는 Git에 포함하지 않습니다. Python과 CLI가 수집하는 진단 로그에 사용자 응답 본문을 추가하지 않습니다.

GitHub에 푸시하는 것만으로 자동 배포되지는 않습니다. 코드 변경 후 위 배포 명령을 실행해야 공개 앱에 반영됩니다.
