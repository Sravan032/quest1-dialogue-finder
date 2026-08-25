import unittest

from src.acquisition.video_id import extract_video_id


class TestVideoId(unittest.TestCase):

    def test_okru_url(self):

        url = "https://ok.ru/video/248244667877"

        result = extract_video_id(url)

        self.assertEqual(
            result,
            "248244667877"
        )

    def test_youtube_url(self):

        url = (
            "https://www.youtube.com/"
            "watch?v=R8SE3RxqaTY"
        )

        result = extract_video_id(url)

        self.assertEqual(
            result,
            "R8SE3RxqaTY"
        )

    def test_invalid_url(self):

        url = "https://example.com/video"

        with self.assertRaises(ValueError):
            extract_video_id(url)


if __name__ == "__main__":
    unittest.main()