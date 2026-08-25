import cv2

VIDEO_PATH = "data/videos/quest1.mp4"

TARGET_TIME = 324.56

cap = cv2.VideoCapture(VIDEO_PATH)

fps = cap.get(cv2.CAP_PROP_FPS)

# Find the nearest frame to the Whisper timestamp
frame_number = round(TARGET_TIME * fps)

# Convert that frame number back to its actual video timestamp
actual_timestamp = frame_number / fps

difference = actual_timestamp - TARGET_TIME

print(f"FPS              : {fps}")
print(f"Whisper timestamp : {TARGET_TIME:.3f}s")
print(f"Nearest frame     : {frame_number}")
print(f"Frame timestamp   : {actual_timestamp:.3f}s")
print(f"Difference         : {difference:+.3f}s")

# Extract the frame
cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)

success, frame = cap.read()

if success:
    output_path = (
        f"data/frames/248244667877/"
        f"fine/speech_start_{frame_number}.jpg"
    )

    cv2.imwrite(output_path, frame)

    print(f"Saved: {output_path}")
else:
    print("Could not read the frame.")

cap.release()