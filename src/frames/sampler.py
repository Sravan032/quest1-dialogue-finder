import cv2


class FrameSampler:

    def sample(
        self,
        video_path,
        start_time,
        end_time,
        interval=0.2
    ):

        cap = cv2.VideoCapture(
            video_path
        )

        if not cap.isOpened():
            raise ValueError(
                f"Could not open video: {video_path}"
            )

        try:

            fps = cap.get(
                cv2.CAP_PROP_FPS
            )

            if fps <= 0:
                raise ValueError(
                    "Invalid FPS"
                )

            current_time = start_time

            while current_time <= end_time:

                frame_number = round(
                    current_time * fps
                )

                cap.set(
                    cv2.CAP_PROP_POS_FRAMES,
                    frame_number
                )

                success, frame = cap.read()

                if success:

                    yield (
                        frame,
                        frame_number / fps
                    )

                current_time += interval

        finally:

            cap.release()