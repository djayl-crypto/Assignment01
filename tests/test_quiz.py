"""검증: python -m unittest -v"""
import json
import threading
import unittest
from http.server import ThreadingHTTPServer
from urllib.error import HTTPError
from urllib.request import Request, urlopen

from src.app import AppHandler
from src.quiz import CITY_TYPES, QUESTIONS, answer_to_points, calculate_result, check_answer


class QuizTests(unittest.TestCase):
    def test_score_mapping_and_validation(self):
        self.assertEqual([answer_to_points(value) for value in range(1, 6)], [0, 1, 2, 3, 4])
        for value in [True, False, None, "3", 3.0, 0, 6, [], {}]:
            with self.subTest(value=value):
                self.assertFalse(check_answer(value))
                with self.assertRaises(ValueError):
                    answer_to_points(value)

    def test_each_type_can_win_with_equal_maximum(self):
        for key in CITY_TYPES:
            answers = [5 if question["type"] == key else 1 for question in QUESTIONS]
            result = calculate_result(answers)
            self.assertEqual(result["best_types"], [key])
            self.assertEqual(result["mode"], "single")
            self.assertEqual(result["percentages"][key], 100)
            self.assertEqual(list(result["maximums"].values()), [8] * 5)

    def test_ties_and_no_preference(self):
        tied = calculate_result([3] * 10)
        self.assertEqual(tied["mode"], "mixed")
        self.assertEqual(len(tied["best_types"]), 5)
        self.assertEqual(list(tied["percentages"].values()), [50] * 5)
        empty = calculate_result([1] * 10)
        self.assertEqual(empty["mode"], "exploring")
        self.assertEqual(empty["best_types"], [])

    def test_partial_tie(self):
        result = calculate_result([5, 5, 1, 1, 1] * 2)
        self.assertEqual(result["best_types"], ["green", "transit"])

    def test_invalid_payload_and_request_isolation(self):
        for answers in [None, {}, "12345", [5] * 9, [5] * 11, [5] * 9 + [True]]:
            with self.assertRaises(ValueError):
                calculate_result(answers)
        calculate_result([5] * 10)
        self.assertEqual(list(calculate_result([1] * 10)["scores"].values()), [0] * 5)


class HttpTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = ThreadingHTTPServer(("127.0.0.1", 0), AppHandler)
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()
        cls.base = f"http://127.0.0.1:{cls.server.server_port}"

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()
        cls.thread.join()

    def test_static_and_quiz(self):
        for path in ["/", "/style.css", "/script.js", "/city.svg"]:
            with urlopen(self.base + path) as response:
                self.assertEqual(response.status, 200)
                self.assertGreater(len(response.read()), 100)
        with urlopen(self.base + "/api/quiz") as response:
            self.assertEqual(len(json.load(response)["questions"]), 10)

    def test_result_api_and_invalid_input(self):
        request = Request(self.base + "/api/result", data=json.dumps({"answers": [5, 2, 3, 2, 1] * 2}).encode(), headers={"Content-Type": "application/json"})
        with urlopen(request) as response:
            self.assertEqual(json.load(response)["best_types"], ["green"])
        for body in [b"{", b"[]", b'{"answers":[]}']:
            with self.assertRaises(HTTPError) as context:
                urlopen(Request(self.base + "/api/result", data=body))
            self.assertEqual(context.exception.code, 400)
            context.exception.close()

    def test_private_files_not_served(self):
        for path in ["/quiz.py", "/.git/config", "/../README.md"]:
            with self.assertRaises(HTTPError) as context:
                urlopen(self.base + path)
            self.assertEqual(context.exception.code, 404)
            context.exception.close()


if __name__ == "__main__":
    unittest.main()
