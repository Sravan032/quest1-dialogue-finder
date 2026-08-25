from pathlib import Path

from acquisition.video_id import extract_video_id
from utils.paths import ProjectPaths
from speech.localizer import SpeechLocalizer
from frames.mapper import FrameMapper


VIDEO_URL = "https://ok.ru/video/248244667877"
TARGET = "My mind rebels at stagnation"


def main():

    print("=== Quest1 Dialogue Finder ===\n")

    # -------------------------
    # 1. Extract video ID
    # -------------------------

    video_id = extract_video_id(VIDEO_URL)

    print(f"Video ID: {video_id}\n")

    # -------------------------
    # 2. Create project paths
    # -------------------------

    paths = ProjectPaths(video_id)
    paths.create_directories()

    video_path = paths.video_path
    transcription_path = paths.transcription_path

    # -------------------------
    # 3. Speech localization
    # -------------------------

    speech = SpeechLocalizer()

    if transcription_path.exists():

        print("Loading cached transcription...")

        segments = speech.load_transcription(
            transcription_path
        )

    else:

        print("Transcribing video...")

        segments = speech.transcribe(
            video_path
        )

        speech.save_transcription(
            segments,
            transcription_path
        )

        print("Transcription saved.")

    print(
        f"Transcription ready: "
        f"{len(segments)} segments\n"
    )

    # -------------------------
    # 4. Find dialogue
    # -------------------------

    result = speech.find_dialogue(
        segments,
        TARGET
    )

    if result is None:
        print("Dialogue not found.")
        return

    if not result["words"]:
        print("No word timestamps available.")
        return

    speech_start = result["words"][0]["start"]

    # -------------------------
    # 5. Map timestamp → frame
    # -------------------------

    mapper = FrameMapper()

    fps = mapper.get_fps(video_path)

    frame_number = mapper.timestamp_to_frame(
        speech_start,
        fps
    )

    actual_timestamp = mapper.frame_to_timestamp(
        frame_number,
        fps
    )

    # -------------------------
    # 6. Result
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