import easyocr


class OCRReader:

    def __init__(self, languages=None):

        if languages is None:
            languages = ["en"]

        self.reader = easyocr.Reader(
            languages,
            gpu=False
        )

    def read(self, image):

        results = self.reader.readtext(
            image
        )

        detected_text = []

        for _, text, confidence in results:

            detected_text.append({
                "text": text,
                "confidence": confidence
            })

        return detected_text