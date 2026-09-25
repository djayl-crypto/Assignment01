"""로컬 Worker 또는 배포 주소의 화면과 Python API를 검증합니다."""

import argparse
import json
from urllib.error import HTTPError
from urllib.request import Request, urlopen

from quiz import CITY_TYPES, QUESTIONS, calculate_result


def request(base, path, method="GET", payload=None, raw_body=None):
    body = raw_body
    if payload is not None:
        body = json.dumps(payload).encode("utf-8")
    req = Request(base + path, data=body, method=method,
                  headers={"Content-Type": "application/json",
                           "User-Agent": "CITYFIT-Deployment-Check/1.0"})
    try:
        response = urlopen(req, timeout=45)
    except HTTPError as error:
        response = error
    with response:
        return response.status, response.read()


def verify(base):
    for path in ("/", "/style.css", "/script.js", "/city.svg"):
        status, body = request(base, path)
        assert status == 200 and len(body) > 100, (path, status)
    status, body = request(base, "/api/quiz")
    quiz = json.loads(body)
    assert status == 200 and quiz["questions"] == QUESTIONS
    assert quiz["types"] == CITY_TYPES

    samples = [[1] * 10, [3] * 10, [5, 5, 1, 1, 1] * 2]
    for city_type in CITY_TYPES:
        samples.append([5 if item["type"] == city_type else 1 for item in QUESTIONS])
    for answers in samples:
        status, body = request(base, "/api/result", "POST", {"answers": answers})
        assert status == 200, (status, body)
        assert json.loads(body) == calculate_result(answers), body

    for payload in ({"answers": []}, {"answers": [True] * 10}, {"answers": [6] * 10}, []):
        status, _ = request(base, "/api/result", "POST", payload)
        assert status == 400, status
    status, _ = request(base, "/api/result", "POST", raw_body=b"{")
    assert status == 400, status
    status, _ = request(base, "/api/result", "POST", raw_body=b"x" * 4097)
    assert status == 413, status
    status, _ = request(base, "/api/result")
    assert status == 405, status
    for path in ("/api/unknown", "/quiz.py", "/.git/config"):
        status, _ = request(base, path)
        assert status == 404, (path, status)
    print(f"PASS: static pages, Python result parity (8 cases), input validation, methods and 404s at {base}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("base_url")
    args = parser.parse_args()
    verify(args.base_url.rstrip("/"))
