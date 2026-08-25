from difflib import SequenceMatcher


class WordAligner:

    def normalize(self, word):
        return (
            word.lower()
            .strip(".,!?;:\"'()[]{}")
        )

    def similarity(self, word1, word2):
        return SequenceMatcher(
            None,
            self.normalize(word1),
            self.normalize(word2)
        ).ratio()

    def align(self, target, words):

        target_words = target.split()

        if not target_words or not words:
            return None

        best_start = None
        best_score = 0.0

        # Try every possible starting word
        for start_index in range(len(words)):

            matched = 0
            total_score = 0.0

            for target_index, target_word in enumerate(target_words):

                word_index = start_index + target_index

                if word_index >= len(words):
                    break

                score = self.similarity(
                    target_word,
                    words[word_index]["word"]
                )

                total_score += score
                matched += 1

            if matched == 0:
                continue

            average_score = total_score / matched

            if average_score > best_score:

                best_score = average_score
                best_start = start_index

        if best_start is None:
            return None

        return {
            "score": best_score,
            "start_word": words[best_start],
            "start_index": best_start
        }