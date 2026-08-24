print("1. Script started")

from faster_whisper import WhisperModel

print("2. faster-whisper imported")

VIDEO_PATH = "data/videos/quest1.mp4"

print("3. Loading model...")

model = WhisperModel(
    "base",
    device="cpu",
    compute_type="int8"
)

print("4. Model loaded")

print("5. Starting transcription...")

segments, info = model.transcribe(
    VIDEO_PATH,
    beam_size=5
)

print("6. Transcription started")

count = 0

for segment in segments:
    print(
        f"{segment.start:.2f}s -> "
        f"{segment.end:.2f}s : "
        f"{segment.text}"
    )
    count += 1

print(f"7. Total segments: {count}")