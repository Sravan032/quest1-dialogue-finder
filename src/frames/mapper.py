import cv2


class FrameMapper:

    def get_fps(self, video_path):

        cap = cv2.VideoCapture(video_path)

        if not cap.isOpened():
            raise ValueError(f"Could not open video: {video_path}")

        fps = cap.get(cv2.CAP_PROP_FPS)

        cap.release()

        if fps <= 0:
            raise ValueError("Invalid FPS")

        return fps

    def timestamp_to_frame(self, timestamp, fps):

        return round(timestamp * fps)

    def frame_to_timestamp(self, frame_number, fps):

        return frame_number / fps

    def get_frame(self, video_path, frame_number):

        cap = cv2.VideoCapture(video_path)

        if not cap.isOpened():
            raise ValueError(f"Could not open video: {video_path}")

        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)

        success, frame = cap.read()

        cap.release()

        if not success:
            raise ValueError(
                f"Could not read frame {frame_number}"
            )

        return frame