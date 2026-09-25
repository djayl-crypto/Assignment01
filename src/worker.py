"""Cloudflare Workers에서 CITY:FIT의 Python API를 실행합니다."""

import json
from urllib.parse import urlsplit

from workers import Response, WorkerEntrypoint

from quiz import CHOICES, CITY_TYPES, QUESTIONS, calculate_result


def json_response(data, status=200, extra_headers=None):
    headers = {
        "Content-Type": "application/json; charset=utf-8",
        "Cache-Control": "no-store",
        "X-Content-Type-Options": "nosniff",
    }
    if extra_headers:
        headers.update(extra_headers)
    return Response(json.dumps(data, ensure_ascii=False), status=status, headers=headers)


class Default(WorkerEntrypoint):
    async def fetch(self, request):
        path = urlsplit(request.url).path

        if path == "/api/quiz":
            if request.method != "GET":
                return json_response({"error": "GET 요청을 사용해주세요."}, 405, {"Allow": "GET"})
            return json_response({"questions": QUESTIONS, "choices": CHOICES, "types": CITY_TYPES})

        if path == "/api/result":
            if request.method != "POST":
                return json_response({"error": "POST 요청을 사용해주세요."}, 405, {"Allow": "POST"})
            # 브라우저가 전송한 요청 길이를 먼저 확인하여 큰 본문을 읽지 않습니다.
            length = request.headers.get("Content-Length")
            if length is None:
                return json_response({"error": "요청 길이가 필요합니다."}, 411)
            try:
                length = int(length)
                if length <= 0 or length > 4096:
                    return json_response({"error": "요청 크기가 올바르지 않습니다."}, 413)
                body = await request.text()
                if len(body.encode("utf-8")) > 4096:
                    return json_response({"error": "요청 크기가 올바르지 않습니다."}, 413)
                payload = json.loads(body)
                if not isinstance(payload, dict):
                    raise ValueError("응답 형식이 올바르지 않습니다.")
                return json_response(calculate_result(payload.get("answers")))
            except (ValueError, UnicodeDecodeError):
                return json_response({"error": "10개의 질문에 1~5 사이의 정수로 답해주세요."}, 400)

        # 정적 화면은 Cloudflare Static Assets에서 직접 제공하고,
        # 일치하지 않는 API나 파일 경로는 404로 처리합니다.
        return json_response({"error": "페이지를 찾을 수 없습니다."}, 404)
