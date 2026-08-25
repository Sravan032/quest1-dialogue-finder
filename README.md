# Quest1 Dialogue Finder

A Python-based video localization tool that identifies the **video frame corresponding to a given dialogue**.

The application accepts a video URL and target dialogue, then combines speech transcription and visual text detection to localize the dialogue and extract the corresponding video frame.

## Features

- Download videos from a URL
- Cache downloaded videos locally
- Speech transcription using `faster-whisper`
- Word-level dialogue localization
- Fuzzy matching for transcription errors
- OCR-based visual dialogue search
- Coarse-to-fine visual search
- Speech and visual result fusion
- Timestamp-to-frame mapping
- Exact target-frame extraction
- Transcription caching
- Error handling
- Automated unit tests

## Requirements

- Python 3.x
- FFmpeg
- Internet connection for video acquisition
- Dependencies listed in `requirements.txt`

## Installation

### 1. Clone the repository

```bash
git clone <repository-url>
cd quest1-dialogue-finder
```

### 2. Create a virtual environment

```powershell
python -m venv .venv
```

### 3. Activate the virtual environment

On Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

### 4. Install dependencies

```powershell
pip install -r requirements.txt
```

## Usage

Run the application with a video URL and target dialogue:

```bash
python src/main.py "<video_url>" "<dialogue>"
```

### Example

```bash
python src/main.py "https://ok.ru/video/248244667877" "My mind rebels at stagnation"
```

To view the available command-line options:

```bash
python src/main.py --help
```

## Example Output

```text
=== Quest1 Dialogue Finder ===

Video ID: 248244667877

Using existing video: data\videos\248244667877.mp4

Loading cached transcription...
Transcription ready: 678 segments

Final localization
-------------------
Target dialogue : My mind rebels at stagnation
Speech match    : 0.947
Matched text    : My mind rebels its stagnation
Visual search   : NOT FOUND
Source          : speech
Timestamp       : 324.560s
Frame           : 7782
Frame timestamp : 324.574s
Frame error     : +0.014s
Target frame    : data\frames\248244667877\final\frame_7782.jpg
```

The output provides:

- Target dialogue
- Speech matching score
- Matched transcription
- Visual search status
- Localization source
- Timestamp
- Frame number
- Actual frame timestamp
- Frame-timestamp error
- Path to the extracted target frame

## Testing

Run the complete test suite:

```bash
python -m unittest discover -s tests -v
```

The test suite covers:

- Speech matching
- Word-level alignment
- OCR matching
- Visual search
- Speech/visual fusion
- OCR failure fallback
- Frame extraction
- Download error handling

## Project Structure

```text
quest1-dialogue-finder/
│
├── README.md
├── APPROACH.md
├── prompts.txt
├── requirements.txt
├── .gitignore
│
├── src/
│   ├── main.py
│   │
│   ├── acquisition/
│   │   ├── downloader.py
│   │   └── video_id.py
│   │
│   ├── core/
│   │   └── exceptions.py
│   │
│   ├── frames/
│   │   ├── mapper.py
│   │   ├── sampler.py
│   │   └── saver.py
│   │
│   ├── localization/
│   │   ├── confidence.py
│   │   └── fusion.py
│   │
│   ├── speech/
│   │   ├── aligner.py
│   │   └── localizer.py
│   │
│   ├── utils/
│   │   └── paths.py
│   │
│   └── vision/
│       ├── ocr.py
│       └── search.py
│
├── tests/
│   ├── test_aligner.py
│   ├── test_errors.py
│   ├── test_frame_saver.py
│   ├── test_fusion.py
│   ├── test_matching.py
│   ├── test_ocr_matching.py
│   └── test_visual_pipeline.py
│
└── data/
```

## Documentation

The project separates implementation usage from detailed engineering documentation.

### Engineering Approach

[`APPROACH.md`](APPROACH.md) documents:

- System architecture
- Engineering decisions
- Implementation reasoning
- Approach trade-offs
- Optimization decisions
- Limitations
- Future improvements

### AI-Assisted Development

[`prompts.txt`](prompts.txt) contains the prompts used during AI-assisted development of the project.

The prompts document the progression from initial problem analysis and architectural exploration through implementation, debugging, and optimization.

## Generated Data

The `data/` directory contains locally generated artifacts such as:

- Downloaded videos
- Cached transcriptions
- Extracted frames

These generated files should not be committed to the repository.

Ensure `.gitignore` excludes project-specific generated data and environment files, for example:

```text
.venv/
__pycache__/
*.pyc
.env
data/videos/
data/transcriptions/
data/frames/
```

## Technologies

- **Python**
- **faster-whisper**
- **EasyOCR**
- **OpenCV**
- **yt-dlp**
- **unittest**

## Overview

The localization pipeline follows a speech-first, visual-verification approach:

```text
Video URL + Target Dialogue
            │
            ▼
     Video Acquisition
            │
            ▼
     Speech Transcription
            │
            ▼
    Dialogue Localization
            │
            ▼
    Word-Level Alignment
            │
            ▼
     Candidate Time Window
            │
            ▼
      Visual OCR Search
            │
            ▼
    Speech / Visual Fusion
            │
            ▼
      Timestamp → Frame
            │
            ▼
       Target Frame
```

For the detailed engineering rationale behind this architecture, see [`APPROACH.md`](APPROACH.md).
