import unittest

from src.speech.aligner import WordAligner


class TestWordAligner(unittest.TestCase):

    def test_internal_dialogue_start(self):

        words = [
            {
                "word": "My",
                "start": 324.56,
                "end": 325.38
            },
            {
                "word": "mind",
                "start": 325.38,
                "end": 325.68
            },
            {
                "word": "rebells",
                "start": 325.68,
                "end": 326.46
            },
            {
                "word": "its",
                "start": 326.46,
                "end": 326.66
            },
            {
                "word": "stagnation",
                "start": 326.66,
                "end": 327.92
            }
        ]

        aligner = WordAligner()

        result = aligner.align(
            "rebels at stagnation",
            words
        )

        self.assertIsNotNone(result)

        self.assertEqual(
            result["start_index"],
            2
        )

        self.assertAlmostEqual(
            result["start_word"]["start"],
            325.68,
            places=2
        )


if __name__ == "__main__":
    unittest.main()