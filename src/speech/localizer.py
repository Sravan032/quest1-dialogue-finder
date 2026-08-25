from difflib import SequenceMatcher
from faster_whisper import WhisperModel
import json
from pathlib import Path
from src.speech.aligner import WordAligner
from src.core.exceptions import TranscriptionError

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
        self.aligner = WordAligner()

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
        try:
            segments, info = self.model.transcribe(
                video_path,
                beam_size=5,
                word_timestamps=True
            )
        except Exception as e:

            raise TranscriptionError(
                f"Transcription failed: {e}"
            ) from e

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

    def find_dialogue(self, segments, target, max_window=3):

        best_match = None
        best_score = 0.0

        for start_index in range(len(segments)):

            combined_text = ""

            for window_size in range(1, max_window + 1):

                end_index = start_index + window_size

                if end_index > len(segments):
                    break

                segment_window = segments[
                    start_index:end_index
                ]

                combined_text = " ".join(
                    segment["text"]
                    for segment in segment_window
                )

                score = self.similarity(
                    target,
                    combined_text
                )

                if score > best_score:

                    best_score = score

                    first_segment = segment_window[0]
                    last_segment = segment_window[-1]

                    # Combine all word timestamps
                    words = []

                    for segment in segment_window:
                        words.extend(
                            segment["words"]
                        )

                    alignment = self.aligner.align(
                        target,
                        words
                    )

                    dialogue_start = None

                    if alignment:
                        dialogue_start = alignment["start_word"]["start"]

                    best_match = {
                        "score": score,
                        "segment_start": first_segment["start"],
                        "segment_end": last_segment["end"],
                        "dialogue_start": dialogue_start,
                        "dialogue_end": words[-1]["end"] if words else None,
                        "text": combined_text,
                        "words": words
                    }

        if best_match is None:
            return None

        if best_match["score"] < 0.70:
            return None

        return best_match