import unittest
from pathlib import Path
import tempfile

from src.frames.saver import FrameSaver


VIDEO_PATH = "data/ocr_test.mp4"


class TestFrameSaver(unittest.TestCase):

    def test_save_frame(self):

        saver = FrameSaver()

        with tempfile.TemporaryDirectory() as temp_dir:

            output_path = (
                Path(temp_dir)
                / "frame_60.jpg"
            )

            result = saver.save(
                VIDEO_PATH,
                60,
                output_path
            )

            self.assertTrue(
                result.exists()
            )

            self.assertGreater(
                result.stat().st_size,
                0
            )


if __name__ == "__main__":
    unittest.main()