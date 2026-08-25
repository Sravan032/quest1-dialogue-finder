import unittest

from src.speech.localizer import SpeechLocalizer


class TestSpeechMatching(unittest.TestCase):

    def test_exact_dialogue(self):

        localizer = SpeechLocalizer()

        segments = [
            {
                "start": 10.0,
                "end": 14.0,
                "text": "My mind rebels its stagnation.",
                "words": [
                    {
                        "word": "My",
                        "start": 10.0,
                        "end": 10.5
                    },
                    {
                        "word": "mind",
                        "start": 10.5,
                        "end": 11.0
                    },
                    {
                        "word": "rebels",
                        "start": 11.0,
                        "end": 12.0
                    },
                    {
                        "word": "its",
                        "start": 12.0,
                        "end": 12.5
                    },
                    {
                        "word": "stagnation",
                        "start": 12.5,
                        "end": 14.0
                    }
                ]
            }
        ]

        result = localizer.find_dialogue(
            segments,
            "My mind rebels at stagnation"
        )

        self.assertIsNotNone(result)

        self.assertGreater(
            result["score"],
            0.80
        )

    def test_dialogue_not_found(self):

        localizer = SpeechLocalizer()

        segments = [
            {
                "start": 10.0,
                "end": 14.0,
                "text": "This is completely different.",
                "words": [
                    {
                        "word": "This",
                        "start": 10.0,
                        "end": 10.5
                    },
                    {
                        "word": "is",
                        "start": 10.5,
                        "end": 11.0
                    },
                    {
                        "word": "completely",
                        "start": 11.0,
                        "end": 12.0
                    },
                    {
                        "word": "different",
                        "start": 12.0,
                        "end": 14.0
                    }
                ]
            }
        ]

        result = localizer.find_dialogue(
            segments,
            "My mind rebels at stagnation"
        )

        self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main()