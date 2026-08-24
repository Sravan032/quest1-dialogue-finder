from difflib import SequenceMatcher
from faster_whisper import WhisperModel

VIDEO_PATH = "data/videos/quest1.mp4"

TARGET = "My mind rebels at stagnation"


def normalize(text):
    return " ".join(
        text.lower()
        .strip()
        .replace(".", "")
        .replace(",", "")
        .split()
    )


def similarity(text1, text2):
    return SequenceMatcher(
        None,
        normalize(text1),
        normalize(text2)
    ).ratio()


model = WhisperModel(
    "base",
    device="cpu",
    compute_type="int8"
)

segments, info = model.transcribe(
    VIDEO_PATH,
    beam_size=5,
    word_timestamps=True
)

best_segment = None
best_score = 0.0

for segment in segments:
    score = similarity(TARGET, segment.text)

    if score > best_score:
        best_score = score
        best_segment = segment


print("Best match:")
print(f"Score : {best_score:.3f}")
print(f"Start : {best_segment.start:.2f}s")
print(f"End   : {best_segment.end:.2f}s")
print(f"Text  : {best_segment.text.strip()}")

print("\nWord timestamps:")

for word in best_segment.words:
    print(
        f"{word.start:.2f}s -> "
        f"{word.end:.2f}s : "
        f"{word.word}"
    )