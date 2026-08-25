import unittest
from unittest.mock import patch, MagicMock

from src.acquisition.downloader import VideoDownloader
from src.speech.localizer import SpeechLocalizer
from src.core.exceptions import (
    VideoDownloadError,
    TranscriptionError
)

class TestDownloadErrors(unittest.TestCase):

    @patch("src.acquisition.downloader.yt_dlp.YoutubeDL")
    def test_download_failure(self, mock_ytdlp):

        mock_ytdlp.side_effect = Exception(
            "Network connection failed"
        )

        downloader = VideoDownloader()

        with self.assertRaises(VideoDownloadError):

            downloader.download(
                "https://example.com/video",
                "data/test/video.mp4"
            )

    def test_transcription_failure(self):

        speech = SpeechLocalizer.__new__(
            SpeechLocalizer
        )

        speech.model = MagicMock()

        speech.model.transcribe.side_effect = Exception(
            "Whisper failed"
        )

        with self.assertRaises(TranscriptionError):

            speech.transcribe(
                "fake_video.mp4"
            )


if __name__ == "__main__":
    unittest.main()