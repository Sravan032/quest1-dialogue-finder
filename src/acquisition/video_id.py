from urllib.parse import urlparse, parse_qs


def extract_video_id(url):

    parsed = urlparse(url)

    # -------------------------
    # YouTube
    # -------------------------

    if parsed.netloc in {
        "youtube.com",
        "www.youtube.com"
    }:

        query = parse_qs(parsed.query)

        if "v" in query and query["v"]:
            return query["v"][0]

    # -------------------------
    # OK.ru
    # -------------------------

    path_parts = [
        part
        for part in parsed.path.split("/")
        if part
    ]

    if "video" in path_parts:

        index = path_parts.index("video")

        if index + 1 < len(path_parts):
            return path_parts[index + 1]

    raise ValueError(
        f"Unsupported or invalid video URL: {url}"
    )