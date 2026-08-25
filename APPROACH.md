# Engineering Approach

## 1. Problem

The goal of Quest1 Dialogue Finder is to locate the exact frame in a video where a given dialogue occurs.

The challenge is that the target dialogue is text, while the final output needs to be a video frame.

The solution therefore follows:

```text
Video URL
    ↓
Video Acquisition
    ↓
Speech Transcription
    ↓
Dialogue Matching
    ↓
Word-Level Alignment
    ↓
Small Visual Search Window
    ↓
OCR Coarse Search
    ↓
OCR Fine Search
    ↓
Speech / OCR Fusion
    ↓
Timestamp → Frame
    ↓
Final Image
```

---

## 2. Why Speech Comes First

The first approach was to use speech transcription to locate the dialogue. `faster-whisper` provides both segment timestamps and word-level timestamps. This gives us a relatively cheap way to identify approximately where the dialogue occurs.

OCR is then restricted to a small region around that timestamp instead of scanning the entire video.

```text
Entire Video
     ↓
Speech
     ↓
Dialogue Timestamp
     ↓
Small Search Window
     ↓
OCR
```

This significantly reduces the amount of visual processing required.

---

## 3. Speech Localization

Speech processing is implemented in:

```text
src/speech/localizer.py
src/speech/aligner.py
```

Whisper transcription is stored with:
- segment timestamps
- segment text
- word timestamps

Exact string matching is not sufficient because speech recognition can introduce small errors.

For example:
- **Target:** `My mind rebels at stagnation`
- **Whisper:** `My mind rebels its stagnation`

Therefore, the implementation normalizes the text and uses `SequenceMatcher` for fuzzy similarity. The best matching window of transcription segments is selected. A minimum similarity threshold prevents unrelated dialogue from being accepted.

---

## 4. Word-Level Alignment

Segment timestamps can be too coarse. The target dialogue may start in the middle of a Whisper segment.

`WordAligner` therefore uses the individual word timestamps to estimate the actual beginning of the requested dialogue. This gives us a better starting timestamp for the visual search.

---

## 5. OCR Search

OCR is implemented in:

```text
src/vision/ocr.py
src/vision/search.py
```

`EasyOCR` is used to detect visible subtitle text. The visual search uses a coarse-to-fine strategy.

### Coarse Search
Frames are sampled at intervals around the speech timestamp. Each frame is passed through OCR and compared with the target dialogue.

### Fine Search
If the coarse search finds a promising candidate, a small window around that timestamp is searched much more densely.

```text
Speech Timestamp
       ↓
Coarse OCR
       ↓
Approximate Visual Location
       ↓
Fine OCR
       ↓
Precise Frame
```

This avoids expensive frame-by-frame OCR over the entire video.

---

## 6. Why Speech and OCR Are Sequential

Speech and OCR are two different information sources, but they are not currently executed in parallel.

The current execution is:

```text
Speech
  ↓
Dialogue Timestamp
  ↓
Small Search Window
  ↓
OCR
  ↓
Fusion
```

This is intentional. Speech reduces the search space before OCR starts. Running OCR over the entire video independently would require significantly more computation without providing enough additional benefit for the current problem.

Parallel processing could be explored later, but it was not necessary for the current implementation.

---

## 7. Speech / OCR Fusion

Fusion is implemented in:

```text
src/localization/fusion.py
src/localization/confidence.py
```

The current strategy is deterministic.

If OCR successfully finds the dialogue:
```text
source = OCR
```

The OCR confidence is calculated as:
$$\text{OCR confidence} = 0.6 \times \text{OCR similarity} + 0.4 \times \text{OCR confidence}$$

The higher weight on similarity reflects the importance of matching the detected text to the requested dialogue.

If OCR does not find the dialogue, the system falls back to speech:
```text
source = Speech
confidence = speech similarity
```

This means OCR improves localization when subtitles are available, but an OCR failure does not break the entire application.

---

## 8. Timestamp to Frame

Once fusion selects the final timestamp, `FrameMapper` converts it into a frame using the video's FPS:

$$\text{frame} = \text{round}(\text{timestamp} \times \text{FPS})$$

The application then converts the frame back into a timestamp and reports the difference between the requested timestamp and the actual frame timestamp. This gives a measurable frame-level localization error.

---

## 9. Caching

Two expensive operations are cached.

### Video
If the video already exists locally, it is reused instead of downloaded again.

### Transcription
Whisper transcription is saved as JSON. Subsequent runs load the cached transcription instead of transcribing the video again. This makes repeated testing and demonstrations significantly faster.

---

## 10. Error Handling

Application-specific exceptions are defined in:

```text
src/core/exceptions.py
```

Examples include:
- `VideoDownloadError`
- `TranscriptionError`

External library failures are converted into application-level errors and handled by `main.py`.

OCR is also treated as an optional modality. If visual search fails, the system can fall back to the speech result. The downloader was also made more robust with retries and a browser-like `User-Agent` after encountering connection-reset errors from OK.ru.

---

## 11. Testing

The project uses unit tests for the major components. The tests cover:
- speech matching
- word alignment
- OCR matching
- OCR typo handling
- fusion
- speech fallback
- OCR failure fallback
- frame saving
- download errors
- visual search

The complete suite is run with:

```bash
python -m unittest discover -s tests -v
```

The final test suite passes successfully. The application was also tested end-to-end using a real video.

---

## 12. Performance Optimization

OCR was identified as one of the slower parts of the pipeline. The coarse-to-fine approach was introduced to reduce unnecessary OCR operations.

During development, coarse OCR search time was measured and reduced from approximately 48 seconds to approximately 19.6 seconds while preserving the final result. This optimization was based on actual measurements rather than assumptions.

---

## 13. Important Engineering Trade-offs

### Fuzzy Matching Instead of Exact Matching
Exact matching is too strict because Whisper and OCR can introduce small errors. `SequenceMatcher` provides a simple and explainable solution.

### Speech First Instead of Full-Video OCR
Speech provides a cheap temporal signal and significantly reduces the visual search space.

### Coarse-to-Fine Instead of Frame-by-Frame OCR
Full-frame OCR is expensive, especially on CPU. Sampling first and refining later provides a better accuracy/performance trade-off.

### Rule-Based Fusion Instead of a Learned Model
The current system only needs to combine a small number of confidence signals. A deterministic rule is easier to test and explain. The fusion layer is isolated so a more sophisticated model could be added later.

---

## 14. Limitations

The current implementation has several limitations:
- Speech recognition quality depends on audio quality.
- OCR depends on subtitle visibility and video quality.
- OCR can be computationally expensive on CPU.
- Fuzzy string matching does not handle heavily paraphrased dialogue.
- Video acquisition depends on the source platform and `yt-dlp`.
- The current system is designed for a specific dialogue query rather than large-scale batch processing.

---

## 15. Future Improvements

Possible improvements include:
- GPU acceleration
- Better subtitle-region detection
- Semantic dialogue matching
- Improved confidence calibration
- Multiple dialogue queries
- Better handling of multiple speakers
- API/web interface
- Further acquisition robustness

---

## 16. Final Architecture

```text
                         Video URL
                            |
                            ↓
                    Video Downloader
                            |
                            ↓
                       Local Video
                            |
                            ↓
                    SpeechLocalizer
                            |
                            ↓
                  Fuzzy Dialogue Match
                            |
                            ↓
                       WordAligner
                            |
                            ↓
                   Dialogue Timestamp
                            |
                            ↓
                 Small Search Window
                            |
                            ↓
                    FrameSampler
                            |
                            ↓
                   OCR Coarse Search
                            |
                            ↓
                    OCR Fine Search
                            |
                            ↓
                  Localization Fusion
                     /          \
                  OCR            Speech
                   \              /
                    \            /
                     ↓          ↓
                    Final Timestamp
                            |
                            ↓
                       FrameMapper
                            |
                            ↓
                        FrameSaver
                            |
                            ↓
                       Target Frame
```

The architecture keeps video acquisition, speech processing, visual search, fusion, frame mapping, and frame saving as separate responsibilities. This makes the system easier to test, debug, optimize, and extend without making the implementation unnecessarily complex.
