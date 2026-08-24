import cv2
from pathlib import Path

VIDEO_PATH = "data/videos/quest1.mp4"
VIDEO_ID = "248244667877"

START_TIME = 325.0
END_TIME = 330.0
INTERVAL = 1.0

OUTPUT_DIR = Path(f"data/frames/{VIDEO_ID}/coarse")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

cap = cv2.VideoCapture(VIDEO_PATH)

fps = cap.get(cv2.CAP_PROP_FPS)

current_time = START_TIME

while current_time <= END_TIME:

    cap.set(cv2.CAP_PROP_POS_MSEC, current_time * 1000)

    success, frame = cap.read()

    if not success:
        print(f"Could not read frame at {current_time:.2f}s")
        current_time += INTERVAL
        continue

    filename = OUTPUT_DIR / f"frame_{current_time:.2f}.jpg"

    cv2.imwrite(str(filename), frame)

    print(f"Saved: {filename}")

    current_time += INTERVAL

cap.release()

print("Coarse frame extraction complete.")