from pathlib import Path

import yt_dlp

from src.core.exceptions import VideoDownloadError


class VideoDownloader:

    def download(self, url, output_path):

        output_path = Path(output_path)

        output_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        output_template = str(
            output_path.with_suffix("")
        ) + ".%(ext)s"

        options = {
            "format": (
                "bestvideo+bestaudio/"
                "bestvideo[ext=mp4]+bestaudio[ext=m4a]/"
                "bestvideo+bestaudio[ext=m4a]/"
                "best"
            ),
            "outtmpl": output_template,
            "merge_output_format": "mp4",
            "noplaylist": True,

            "retries": 5,
            "fragment_retries": 5,

            "http_headers": {
                "User-Agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 "
                    "(KHTML, like Gecko) "
                    "Chrome/151.0.0.0 Safari/537.36"
                )
            },
        }

        try:

            with yt_dlp.YoutubeDL(options) as ydl:
                ydl.download([url])

        except Exception as e:

            raise VideoDownloadError(
                f"Could not download video: {e}"
            ) from e

        if not output_path.exists():

            raise VideoDownloadError(
                f"Video was not downloaded to {output_path}"
            )

        return output_path