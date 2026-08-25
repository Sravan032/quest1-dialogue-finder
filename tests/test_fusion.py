import unittest

from src.localization.fusion import LocalizationFusion


class TestFusion(unittest.TestCase):

    def setUp(self):

        self.fusion = LocalizationFusion()

    def test_speech_fallback(self):

        speech = {
            "dialogue_start": 324.56,
            "text": "My mind rebells its stagnation",
            "score": 0.93
        }

        visual = {
            "found": False
        }

        result = self.fusion.choose(
            speech,
            visual
        )

        self.assertEqual(
            result["source"],
            "speech"
        )

        self.assertAlmostEqual(
            result["timestamp"],
            324.56,
            places=2
        )

    def test_ocr_wins(self):

        speech = {
            "dialogue_start": 324.56,
            "text": "My mind rebells its stagnation",
            "score": 0.93
        }

        visual = {
            "found": True,
            "timestamp": 324.50,
            "frame": 60,
            "text": "My mind rebels at stagnation",
            "confidence": 0.92,
            "similarity": 0.95
        }

        result = self.fusion.choose(
            speech,
            visual
        )

        self.assertEqual(
            result["source"],
            "ocr"
        )

        self.assertEqual(
            result["frame"],
            60
        )

    def test_ocr_failure_falls_back_to_speech(self):

        speech = {
            "dialogue_start": 324.56,
            "text": "My mind rebells its stagnation",
            "score": 0.93
        }

        visual = {
            "found": False
        }

        result = self.fusion.choose(
            speech,
            visual
        )

        self.assertEqual(
            result["source"],
            "speech"
        )

        self.assertAlmostEqual(
            result["timestamp"],
            324.56,
            places=2
        )


if __name__ == "__main__":
    unittest.main()