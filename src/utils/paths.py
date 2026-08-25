from pathlib import Path


class ProjectPaths:

    def __init__(self, video_id):
        self.video_id = video_id

        self.data_dir = Path("data")

        self.video_path = (
            self.data_dir
            / "videos"
            / f"{video_id}.mp4"
        )

        self.transcription_path = (
            self.data_dir
            / "transcriptions"
            / f"{video_id}.json"
        )

        self.frames_dir = (
            self.data_dir
            / "frames"
            / video_id
        )

        self.coarse_frames_dir = (
            self.frames_dir
            / "coarse"
        )

        self.fine_frames_dir = (
            self.frames_dir
            / "fine"
        )

    def create_directories(self):

        self.video_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        self.transcription_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        self.coarse_frames_dir.mkdir(
            parents=True,
            exist_ok=True
        )

        self.fine_frames_dir.mkdir(
            parents=True,
            exist_ok=True
        )