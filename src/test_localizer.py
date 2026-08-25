from speech.localizer import SpeechLocalizer


VIDEO_PATH = "data/videos/quest1.mp4"

TARGET = "My mind rebels at stagnation"


localizer = SpeechLocalizer()

segments = localizer.transcribe(VIDEO_PATH)

result = localizer.find_dialogue(
    segments,
    TARGET
)

print("Dialogue localization result")
print("--------------------------------")

print(f"Score : {result['score']:.3f}")
print(f"Start : {result['start']:.2f}s")
print(f"End   : {result['end']:.2f}s")
print(f"Text  : {result['text']}")

print("\nWords:")

for word in result["words"]:
    print(
        f"{word.start:.2f}s -> "
        f"{word.end:.2f}s : "
        f"{word.word}"
    )