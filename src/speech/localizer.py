from difflib import SequenceMatcher
from faster_whisper import WhisperModel


class SpeechLocalizer:

    def __init__(
        self,
        model_size="base",
        device="cpu",
        compute_type="int8"
    ):
        self.model = WhisperModel(
            model_size,
            device=device,
            compute_type=compute_type
        )

    def normalize(self, text):
        return " ".join(
            text.lower()
            .strip()
            .replace(".", "")
            .replace(",", "")
            .split()
        )

    def similarity(self, text1, text2):
        return SequenceMatcher(
            None,
            self.normalize(text1),
            self.normalize(text2)
        ).ratio()

    def transcribe(self, video_path):

        segments, info = self.model.transcribe(
            video_path,
            beam_size=5,
            word_timestamps=True
        )

        return list(segments)

    def find_dialogue(self, segments, target):

        best_segment = None
        best_score = 0.0

        for segment in segments:

            score = self.similarity(
                target,
                segment.text
            )

            if score > best_score:
                best_score = score
                best_segment = segment

        if best_segment is None:
            return None

        return {
            "score": best_score,
            "start": best_segment.start,
            "end": best_segment.end,
            "text": best_segment.text.strip(),
            "words": best_segment.words
        }