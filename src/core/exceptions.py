class Quest1Error(Exception):
    """Base exception for Quest1."""


class VideoDownloadError(Quest1Error):
    """Raised when the video cannot be downloaded."""


class TranscriptionError(Quest1Error):
    """Raised when transcription fails."""


class DialogueNotFoundError(Quest1Error):
    """Raised when the target dialogue cannot be found."""


class FrameExtractionError(Quest1Error):
    """Raised when video frames cannot be extracted."""


class OCRSearchError(Quest1Error):
    """Raised when visual text search fails."""