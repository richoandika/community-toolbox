"""
Text Analyzer - A utility for analyzing text content.

Provides functionality to analyze text for word count, character count,
reading time, and basic statistics.
"""

import re
from typing import Dict, List, Tuple
from dataclasses import dataclass


@dataclass
class TextStats:
    """Container for text analysis statistics."""
    word_count: int
    character_count: int
    character_count_no_spaces: int
    sentence_count: int
    paragraph_count: int
    reading_time_minutes: float
    most_common_words: List[Tuple[str, int]]


class TextAnalyzer:
    """Main class for text analysis functionality."""

    def __init__(self):
        self.words_per_minute = 200  # Average reading speed

    def analyze(self, text: str) -> TextStats:
        """
        Analyze the given text and return comprehensive statistics.

        Args:
            text: The text to analyze

        Returns:
            TextStats object containing analysis results
        """
        if not text or not text.strip():
            return TextStats(
                word_count=0,
                character_count=0,
                character_count_no_spaces=0,
                sentence_count=0,
                paragraph_count=0,
                reading_time_minutes=0.0,
                most_common_words=[]
            )

        # Basic counts
        word_count = len(self._get_words(text))
        character_count = len(text)
        character_count_no_spaces = len(text.replace(' ', '').replace('\n', '').replace('\t', ''))
        sentence_count = self._count_sentences(text)
        paragraph_count = self._count_paragraphs(text)

        # Reading time calculation
        reading_time_minutes = word_count / self.words_per_minute

        # Most common words
        most_common_words = self._get_most_common_words(text)

        return TextStats(
            word_count=word_count,
            character_count=character_count,
            character_count_no_spaces=character_count_no_spaces,
            sentence_count=sentence_count,
            paragraph_count=paragraph_count,
            reading_time_minutes=reading_time_minutes,
            most_common_words=most_common_words
        )

    def _get_words(self, text: str) -> List[str]:
        """Extract words from text, handling punctuation."""
        # Remove punctuation and split into words
        words = re.findall(r'\b\w+\b', text.lower())
        return words

    def _count_sentences(self, text: str) -> int:
        """Count the number of sentences in the text."""
        # Simple sentence counting based on sentence-ending punctuation
        sentences = re.split(r'[.!?]+', text)
        # Filter out empty strings
        sentences = [s.strip() for s in sentences if s.strip()]
        return len(sentences)

    def _count_paragraphs(self, text: str) -> int:
        """Count the number of paragraphs in the text."""
        paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
        return len(paragraphs)

    def _get_most_common_words(self, text: str, limit: int = 10) -> List[Tuple[str, int]]:
        """Get the most common words in the text."""
        words = self._get_words(text)

        # Filter out common stop words
        stop_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
            'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'have',
            'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should',
            'may', 'might', 'must', 'can', 'this', 'that', 'these', 'those', 'i',
            'you', 'he', 'she', 'it', 'we', 'they', 'me', 'him', 'her', 'us', 'them'
        }

        # Count word frequencies
        word_freq = {}
        for word in words:
            if word not in stop_words and len(word) > 2:  # Ignore very short words
                word_freq[word] = word_freq.get(word, 0) + 1

        # Sort by frequency and return top words
        sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
        return sorted_words[:limit]

    def get_word_frequency(self, text: str) -> Dict[str, int]:
        """Get frequency count for all words in the text."""
        words = self._get_words(text)
        word_freq = {}
        for word in words:
            word_freq[word] = word_freq.get(word, 0) + 1
        return word_freq

    def get_reading_level(self, text: str) -> str:
        """
        Estimate the reading level of the text.
        Returns: 'Easy', 'Medium', or 'Hard'
        """
        stats = self.analyze(text)

        if stats.word_count == 0:
            return 'Unknown'

        # Simple heuristic based on average word length and sentence length
        avg_word_length = stats.character_count_no_spaces / stats.word_count
        avg_sentence_length = stats.word_count / max(stats.sentence_count, 1)

        if avg_word_length < 4.5 and avg_sentence_length < 15:
            return 'Easy'
        elif avg_word_length < 5.5 and avg_sentence_length < 20:
            return 'Medium'
        else:
            return 'Hard'


def main():
    """Command-line interface for the text analyzer."""
    import sys

    if len(sys.argv) < 2:
        print("Usage: python text_analyzer.py <text_file>")
        print("   or: python text_analyzer.py --text 'your text here'")
        sys.exit(1)

    analyzer = TextAnalyzer()

    if sys.argv[1] == '--text':
        if len(sys.argv) < 3:
            print("Error: --text requires text content")
            sys.exit(1)
        text = ' '.join(sys.argv[2:])
    else:
        try:
            with open(sys.argv[1], 'r', encoding='utf-8') as f:
                text = f.read()
        except FileNotFoundError:
            print(f"Error: File '{sys.argv[1]}' not found")
            sys.exit(1)
        except Exception as e:
            print(f"Error reading file: {e}")
            sys.exit(1)

    # Analyze the text
    stats = analyzer.analyze(text)
    reading_level = analyzer.get_reading_level(text)

    # Display results
    print("=== Text Analysis Results ===")
    print(f"Word count: {stats.word_count}")
    print(f"Character count: {stats.character_count}")
    print(f"Character count (no spaces): {stats.character_count_no_spaces}")
    print(f"Sentence count: {stats.sentence_count}")
    print(f"Paragraph count: {stats.paragraph_count}")
    print(f"Reading time: {stats.reading_time_minutes:.1f} minutes")
    print(f"Reading level: {reading_level}")

    if stats.most_common_words:
        print("\nMost common words:")
        for word, count in stats.most_common_words:
            print(f"  {word}: {count}")


if __name__ == "__main__":
    main()
