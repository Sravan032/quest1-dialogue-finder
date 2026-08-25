from difflib import SequenceMatcher
from faster_whisper import WhisperModel
import json
from pathlib import Path


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

        results = []

        for segment in segments:

            words = []

            if segment.words:
                for word in segment.words:
                    words.append({
                        "word": word.word,
                        "start": word.start,
                        "end": word.end
                    })

            results.append({
                "start": segment.start,
                "end": segment.end,
                "text": segment.text.strip(),
                "words": words
            })

        return results

    def save_transcription(self, segments, output_path):

        output_path = Path(output_path)

        output_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        with open(
            output_path,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                segments,
                file,
                indent=2,
                ensure_ascii=False
            )

    def load_transcription(self, input_path):

        with open(
            input_path,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(file)

    def find_dialogue(self, segments, target):

        best_segment = None
        best_score = 0.0

        for segment in segments:

            score = self.similarity(
                target,
                segment["text"]
            )

            if score > best_score:
                best_score = score
                best_segment = segment

        if best_segment is None:
            return None

        return {
            "score": best_score,
            "start": best_segment["start"],
            "end": best_segment["end"],
            "text": best_segment["text"],
            "words": best_segment["words"]
        }