from difflib import SequenceMatcher
from src.vision.ocr import OCRReader
import cv2

class OCRSearcher:

    def __init__(self, ocr_reader=None):
        self.ocr = ocr_reader or OCRReader()

    def normalize(self, text):
        return " ".join(
            text.lower()
            .strip()
            .replace(".", "")
            .replace(",", "")
            .split()
        )

    def similarity(self, text1, text2):

        text1 = self.normalize(text1)
        text2 = self.normalize(text2)

        return SequenceMatcher(
            None,
            text1,
            text2
        ).ratio()

    def search(
        self,
        frames,
        target,
        threshold=0.80
    ):

        best_result = None
        best_score = 0.0

        for frame, timestamp in frames:

            results = self.ocr.read(frame)

            for result in results:

                text = result["text"]

                score = self.similarity(
                    target,
                    text
                )

                if score > best_score:

                    best_score = score

                    best_result = {
                        "found": score >= threshold,
                        "timestamp": timestamp,
                        "text": text,
                        "confidence": result["confidence"],
                        "similarity": score
                    }

                    if score >= threshold:
                        return best_result

        if best_result is None:

            return {
                "found": False
            }

        return best_result

    def refine(
        self,
        video_path,
        start_time,
        end_time,
        target,
        interval=None,
        threshold=0.80
    ):

        cap = cv2.VideoCapture(
            str(video_path)
        )

        if not cap.isOpened():
            raise ValueError(
                f"Could not open video: {video_path}"
            )

        fps = cap.get(
            cv2.CAP_PROP_FPS
        )

        if interval is None:
            interval = 1 / fps

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

            if not success:
                current_time += interval
                continue

            results = self.ocr.read(frame)

            for result in results:

                score = self.similarity(
                    target,
                    result["text"]
                )

                if score >= threshold:

                    cap.release()

                    return {
                        "found": True,
                        "frame": frame_number,
                        "timestamp": frame_number / fps,
                        "text": result["text"],
                        "confidence": result["confidence"],
                        "similarity": score
                    }

            current_time += interval

        cap.release()

        return {
            "found": False
        }