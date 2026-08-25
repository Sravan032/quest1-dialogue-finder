import unittest
from pathlib import Path

from src.vision.ocr import OCRReader
from src.vision.search import OCRSearcher


VIDEO_PATH = "data/ocr_test.mp4"
TARGET = "My mind rebels at stagnation"


class TestVisualPipeline(unittest.TestCase):

    def test_exact_visual_frame(self):

        self.assertTrue(
            Path(VIDEO_PATH).exists()
        )

        ocr = OCRReader()

        searcher = OCRSearcher(
            ocr
        )

        # We already know coarse OCR finds
        # the target around 2.583 seconds.
        coarse_timestamp = 2.583

        result = searcher.refine(
            VIDEO_PATH,
            coarse_timestamp - 0.3,
            coarse_timestamp + 0.1,
            TARGET
        )

        self.assertTrue(
            result["found"]
        )

        self.assertEqual(
            result["frame"],
            60
        )

        self.assertAlmostEqual(
            result["timestamp"],
            2.5,
            places=2
        )


if __name__ == "__main__":
    unittest.main()