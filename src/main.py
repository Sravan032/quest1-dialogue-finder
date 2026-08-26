# import cv2

# cv2.setLogLevel(0)
# import sys
import argparse
import time
from pathlib import Path

from src.acquisition.video_id import extract_video_id
from src.acquisition.downloader import VideoDownloader
from src.utils.paths import ProjectPaths
from src.speech.localizer import SpeechLocalizer
from src.frames.mapper import FrameMapper
from src.frames.sampler import FrameSampler
from src.frames.saver import FrameSaver
from src.vision.ocr import OCRReader
from src.vision.search import OCRSearcher
from src.localization.fusion import LocalizationFusion
from src.core.exceptions import VideoDownloadError
from src.core.exceptions import TranscriptionError


# VIDEO_URL = "https://ok.ru/video/248244667877"
# TARGET = "My mind rebels at stagnation"

def parse_arguments():

    parser = argparse.ArgumentParser(
        description=(
            "Find the exact video frame where "
            "a dialogue appears."
        )
    )

    parser.add_argument(
        "video_url",
        help="URL of the video"
    )

    parser.add_argument(
        "dialogue",
        help="Dialogue to locate"
    )

    return parser.parse_args()

def format_timestamp(seconds):
    minutes = int(seconds // 60)
    remaining_seconds = seconds % 60

    return f"{minutes:02d}:{remaining_seconds:06.3f}"

def main():

    args = parse_arguments()

    video_url = args.video_url
    target = args.dialogue

    print("=== Quest1 Dialogue Finder ===\n")
    # if len(sys.argv) != 3:
    #     print(
    #         'Usage: python src/main.py "<video_url>" "<dialogue>"'
    #     )
    #     return

    # video_url = sys.argv[1]
    # target = sys.argv[2]

    # -------------------------
    # 1. Extract video ID
    # -------------------------

    video_id = extract_video_id(video_url)

    print(f"Video ID: {video_id}\n")

    # -------------------------
    # 2. Create project paths
    # -------------------------

    paths = ProjectPaths(video_id)
    paths.create_directories()

    video_path = paths.video_path
    if not video_path.exists():

        print("Video not found locally.")
        print("Downloading video...")

        downloader = VideoDownloader()

        try:
            downloader.download(
                video_url,
                video_path
            )

        except VideoDownloadError as e:

            print(f"\nError: {e}")
            return

        print("Video downloaded.\n")
    else:
        print(
            f"Using existing video: "
            f"{video_path}\n"
        )

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

        try:
            segments = speech.transcribe(
                video_path
            )

        except TranscriptionError as e:

            print(f"\nError: {e}")
            return

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
        target
    )

    if result is None:
        print("Dialogue not found.")
        return

    if not result["words"]:
        print("No word timestamps available.")
        return

    speech_start = result["dialogue_start"]
    speech_end = result["dialogue_end"]

    if speech_start is None:
        print("Could not determine dialogue start.")
        return

    search_start = max(
        0,
        speech_start - 0.5
    )

    search_end = speech_end + 0.5

    sampler = FrameSampler()

    frames = sampler.sample(
        video_path,
        search_start,
        search_end,
        interval=0.5
    )

    ocr = OCRReader()

    visual_searcher = OCRSearcher(
        ocr
    )

    try:

        # -------------------------
        # OCR coarse search timing
        # -------------------------

        ocr_start = time.perf_counter()

        visual_result = visual_searcher.search(
            frames,
            target
        )

        print(
            f"OCR coarse search: "
            f"{time.perf_counter() - ocr_start:.2f}s"
        )

    except Exception as e:

        print(
            f"Visual search failed: {e}"
        )

        visual_result = {
            "found": False
        }

    if visual_result["found"]:

        try:

            coarse_timestamp = (
                visual_result["timestamp"]
            )

            # -------------------------
            # OCR fine search timing
            # -------------------------

            fine_start = time.perf_counter()

            fine_result = visual_searcher.refine(
                video_path,
                coarse_timestamp - 0.5,
                coarse_timestamp + 0.5,
                target
            )

            print(
                f"OCR fine search: "
                f"{time.perf_counter() - fine_start:.2f}s"
            )

            if fine_result["found"]:
                visual_result = fine_result

        except Exception as e:

            print(
                f"Fine visual search failed: {e}"
            )

            visual_result = {
                "found": False
            }

    fusion = LocalizationFusion()

    final_result = fusion.choose(
        result,
        visual_result
    )

    # -------------------------
    # 5. Map timestamp → frame
    # -------------------------

    mapper = FrameMapper()

    fps = mapper.get_fps(video_path)

    if final_result["frame"] is not None:
        frame_number = final_result["frame"]
    else:
        frame_number = mapper.timestamp_to_frame(
            final_result["timestamp"],
            fps
        )

    actual_timestamp = mapper.frame_to_timestamp(
        frame_number,
        fps
    )

    # -------------------------
    # 6. Save final target frame
    # -------------------------

    video_id = Path(video_path).stem

    output_dir = (
        Path("data")
        / "frames"
        / video_id
        / "final"
    )

    output_path = (
        output_dir
        / f"frame_{frame_number}.jpg"
    )

    saver = FrameSaver()

    saved_frame = saver.save(
        video_path,
        frame_number,
        output_path
    )

    # -------------------------
    # 7. Result
    # -------------------------

    print("\nFinal localization")
    print("-------------------")

    print(
        f"Target dialogue : {target}"
    )

    print(
        f"Speech match    : "
        f"{result['score']:.3f}"
    )

    print(
        f"Matched text    : "
        f"{result['text']}"
    )

    print(
        f"Visual search   : "
        f"{'FOUND' if visual_result['found'] else 'NOT FOUND'}"
    )

    print(
        f"Source          : "
        f"{final_result['source']}"
    )

    print(
        f"Timestamp       : "
        f"{final_result['timestamp']:.3f}s "
        f"({format_timestamp(final_result['timestamp'])})"
    )

    print(
        f"Frame           : "
        f"{frame_number}"
    )

    print(
        f"Frame timestamp : "
        f"{actual_timestamp:.3f}s "
        f"({format_timestamp(actual_timestamp)})"
    )

    print(
        f"Frame error     : "
        f"{actual_timestamp - final_result['timestamp']:+.3f}s"
    )

    print(
        f"Target frame    : {saved_frame}"
    )


if __name__ == "__main__":
    main()