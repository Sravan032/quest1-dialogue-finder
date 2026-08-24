import cv2

VIDEO_PATH = "data/videos/quest1.mp4"

cap = cv2.VideoCapture(VIDEO_PATH)

fps = cap.get(cv2.CAP_PROP_FPS)
frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)
width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
duration = frame_count / fps

print(f"FPS       : {fps}")
print(f"Frames    : {int(frame_count)}")
print(f"Resolution: {int(width)}x{int(height)}")
print(f"Duration  : {duration:.2f}s")

cap.release()