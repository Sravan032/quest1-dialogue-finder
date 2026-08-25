from speech.localizer import SpeechLocalizer
from frames.mapper import FrameMapper


VIDEO_PATH = "data/videos/quest1.mp4"
TARGET = "My mind rebels at stagnation"


def main():

    print("=== Quest1 Dialogue Finder ===\n")

    # -------------------------
    # 1. Speech localization
    # -------------------------

    print("Transcribing video...")

    speech = SpeechLocalizer()

    segments = speech.transcribe(VIDEO_PATH)

    print(f"Transcription complete: {len(segments)} segments\n")

    result = speech.find_dialogue(
        segments,
        TARGET
    )

    if result is None:
        print("Dialogue not found.")
        return

    # -------------------------
    # 2. Extract speech start
    # -------------------------

    first_word = result["words"][0]

    speech_start = first_word.start

    # -------------------------
    # 3. Map timestamp to frame
    # -------------------------

    mapper = FrameMapper()

    fps = mapper.get_fps(VIDEO_PATH)

    frame_number = mapper.timestamp_to_frame(
        speech_start,
        fps
    )

    actual_timestamp = mapper.frame_to_timestamp(
        frame_number,
        fps
    )

    # -------------------------
    # 4. Display result
    # -------------------------

    print("Dialogue localization")
    print("---------------------")

    print(f"Target dialogue : {TARGET}")
    print(f"Match score     : {result['score']:.3f}")
    print(f"Matched text    : {result['text']}")
    print(f"Speech start    : {speech_start:.3f}s")
    print(f"Frame           : {frame_number}")
    print(f"Frame timestamp : {actual_timestamp:.3f}s")

    print(
        f"Frame error     : "
        f"{actual_timestamp - speech_start:+.3f}s"
    )


if __name__ == "__main__":
    main()