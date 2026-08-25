from frames.mapper import FrameMapper


VIDEO_PATH = "data/videos/quest1.mp4"

TARGET_TIME = 324.56


mapper = FrameMapper()

fps = mapper.get_fps(VIDEO_PATH)

frame_number = mapper.timestamp_to_frame(
    TARGET_TIME,
    fps
)

actual_timestamp = mapper.frame_to_timestamp(
    frame_number,
    fps
)

print("Frame mapping")
print("----------------")

print(f"FPS              : {fps}")
print(f"Target timestamp : {TARGET_TIME:.3f}s")
print(f"Frame number     : {frame_number}")
print(f"Frame timestamp  : {actual_timestamp:.3f}s")
print(
    f"Difference       : "
    f"{actual_timestamp - TARGET_TIME:+.3f}s"
)