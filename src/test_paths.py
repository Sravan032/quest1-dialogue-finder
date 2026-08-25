from utils.paths import ProjectPaths


VIDEO_ID = "248244667877"


paths = ProjectPaths(VIDEO_ID)

paths.create_directories()

print("Project paths")
print("----------------")

print(f"Video          : {paths.video_path}")
print(f"Transcription  : {paths.transcription_path}")
print(f"Frames         : {paths.frames_dir}")
print(f"Coarse frames  : {paths.coarse_frames_dir}")
print(f"Fine frames    : {paths.fine_frames_dir}")