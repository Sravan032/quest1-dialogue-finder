import cv2
from pathlib import Path

VIDEO_PATH = "data/videos/quest1.mp4"
VIDEO_ID = "248244667877"

START_TIME = 324.0
END_TIME = 325.5

OUTPUT_DIR = Path(f"data/frames/{VIDEO_ID}/fine")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

cap = cv2.VideoCapture(VIDEO_PATH)

fps = cap.get(cv2.CAP_PROP_FPS)

# Convert start time to an approximate frame number
start_frame = int(START_TIME * fps)

cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)

current_frame = start_frame

while True:

    success, frame = cap.read()

    if not success:
        break

    timestamp = current_frame / fps

    if timestamp > END_TIME:
        break

    filename = OUTPUT_DIR / f"frame_{current_frame}_{timestamp:.3f}s.jpg"

    cv2.imwrite(str(filename), frame)

    print(
        f"Saved frame {current_frame} "
        f"at {timestamp:.3f}s"
    )

    current_frame += 1

cap.release()

print("Fine frame extraction complete.")