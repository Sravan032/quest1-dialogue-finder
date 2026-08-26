from difflib import SequenceMatcher
from faster_whisper import WhisperModel
import json
from pathlib import Path
from src.speech.aligner import WordAligner
from src.core.exceptions import TranscriptionError
import subprocess
import tempfile
import cv2

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

    def _get_duration(self, video_path):

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

        frame_count = cap.get(
            cv2.CAP_PROP_FRAME_COUNT
        )

        cap.release()

        if fps <= 0:
            raise ValueError(
                "Invalid video FPS"
            )

        return frame_count / fps

    def _extract_audio_chunk(
        self,
        video_path,
        output_path,
        start_time,
        end_time
    ):

        duration = end_time - start_time

        command = [
            "ffmpeg",
            "-y",
            "-ss",
            str(start_time),
            "-i",
            str(video_path),
            "-t",
            str(duration),
            "-vn",
            "-ac",
            "1",
            "-ar",
            "16000",
            "-acodec",
            "pcm_s16le",
            str(output_path)
        ]

        result = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        if result.returncode != 0:

            raise RuntimeError(
                "FFmpeg audio extraction failed: "
                + result.stderr[-1000:]
            )

    def transcribe(self, video_path, chunk_duration=600):

        results = []

        try:

            duration = self._get_duration(video_path)

            with tempfile.TemporaryDirectory() as temp_dir:

                chunk_start = 0

                while chunk_start < duration:

                    chunk_end = min(
                        chunk_start + chunk_duration,
                        duration
                    )

                    audio_path = (
                        Path(temp_dir)
                        / f"chunk_{chunk_start}.wav"
                    )

                    self._extract_audio_chunk(
                        video_path,
                        audio_path,
                        chunk_start,
                        chunk_end
                    )

                    segments, info = self.model.transcribe(
                        str(audio_path),
                        beam_size=5,
                        word_timestamps=True
                    )

                    for segment in segments:

                        words = []

                        if segment.words:

                            for word in segment.words:

                                words.append({
                                    "word": word.word,
                                    "start": (
                                        word.start
                                        + chunk_start
                                    ),
                                    "end": (
                                        word.end
                                        + chunk_start
                                    )
                                })

                        results.append({
                            "start": (
                                segment.start
                                + chunk_start
                            ),
                            "end": (
                                segment.end
                                + chunk_start
                            ),
                            "text": segment.text.strip(),
                            "words": words
                        })

                    chunk_start += chunk_duration

        except Exception as e:

            raise TranscriptionError(
                f"Transcription failed: {e}"
            ) from e

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