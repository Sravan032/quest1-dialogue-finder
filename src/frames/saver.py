from pathlib import Path

import cv2


class FrameSaver:

    def save(
        self,
        video_path,
        frame_number,
        output_path
    ):

        cap = cv2.VideoCapture(
            str(video_path)
        )

        if not cap.isOpened():
            raise ValueError(
                f"Could not open video: {video_path}"
            )

        cap.set(
            cv2.CAP_PROP_POS_FRAMES,
            frame_number
        )

        success, frame = cap.read()

        cap.release()

        if not success:
            raise ValueError(
                f"Could not read frame {frame_number}"
            )

        output_path = Path(output_path)

        output_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        cv2.imwrite(
            str(output_path),
            frame
        )

        return output_path