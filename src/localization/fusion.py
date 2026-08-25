class LocalizationFusion:

    def choose(
        self,
        speech_result,
        visual_result
    ):

        if visual_result.get("found"):

            return {
                "timestamp": visual_result["timestamp"],
                "frame": visual_result.get("frame"),
                "source": "ocr",
                "text": visual_result["text"],
                "confidence": (
                    0.6
                    * visual_result["similarity"]
                    +
                    0.4
                    * visual_result["confidence"]
                )
            }

        return {
            "timestamp": speech_result["dialogue_start"],
            "frame": None,
            "source": "speech",
            "text": speech_result["text"],
            "confidence": speech_result["score"]
        }