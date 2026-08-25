import unittest

from src.vision.search import OCRSearcher


class FakeOCR:

    def read(self, frame):

        return [
            {
                "text": "My mind rebells at stagnation",
                "confidence": 0.92
            }
        ]


class TestOCRMatching(unittest.TestCase):

    def test_ocr_typo(self):

        searcher = OCRSearcher(
            FakeOCR()
        )

        frames = [
            ("fake_frame", 10.0)
        ]

        result = searcher.search(
            frames,
            "My mind rebels at stagnation"
        )

        self.assertTrue(
            result["found"]
        )

        self.assertGreater(
            result["similarity"],
            0.80
        )


if __name__ == "__main__":
    unittest.main()