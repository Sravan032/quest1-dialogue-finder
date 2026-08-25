from urllib.parse import urlparse


def extract_video_id(url):
    parsed = urlparse(url)

    path_parts = [
        part
        for part in parsed.path.split("/")
        if part
    ]

    if not path_parts:
        raise ValueError("Could not extract video ID")

    # OK.ru: /video/248244667877
    if "video" in path_parts:

        index = path_parts.index("video")

        if index + 1 < len(path_parts):
            return path_parts[index + 1]

    raise ValueError(
        f"Unsupported or invalid video URL: {url}"
    )