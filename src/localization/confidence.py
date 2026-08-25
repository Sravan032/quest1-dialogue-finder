class ConfidenceCalculator:

    def calculate(
        self,
        source,
        speech_score,
        ocr_similarity=None,
        ocr_confidence=None
    ):

        if source == "ocr":

            if (
                ocr_similarity is None
                or ocr_confidence is None
            ):
                return 0.0

            return (
                0.6 * ocr_similarity
                + 0.4 * ocr_confidence
            )

        # Speech fallback
        return speech_score