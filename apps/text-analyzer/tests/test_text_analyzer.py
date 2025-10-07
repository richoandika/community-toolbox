"""
Tests for the Text Analyzer module.
"""

import pytest
import sys
import os

# Add the parent directory to the path so we can import the module
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from text_analyzer import TextAnalyzer, TextStats


class TestTextAnalyzer:
    """Test cases for TextAnalyzer class."""

    def setup_method(self):
        """Set up test fixtures."""
        self.analyzer = TextAnalyzer()

    def test_analyze_empty_text(self):
        """Test analysis of empty text."""
        stats = self.analyzer.analyze("")
        assert stats.word_count == 0
        assert stats.character_count == 0
        assert stats.character_count_no_spaces == 0
        assert stats.sentence_count == 0
        assert stats.paragraph_count == 0
        assert stats.reading_time_minutes == 0.0
        assert stats.most_common_words == []

    def test_analyze_whitespace_only(self):
        """Test analysis of whitespace-only text."""
        stats = self.analyzer.analyze("   \n\t   ")
        assert stats.word_count == 0
        assert stats.character_count == 7
        assert stats.character_count_no_spaces == 0

    def test_analyze_simple_text(self):
        """Test analysis of simple text."""
        text = "Hello world. This is a test."
        stats = self.analyzer.analyze(text)

        assert stats.word_count == 6
        assert stats.character_count == len(text)
        assert stats.character_count_no_spaces == len(text.replace(' ', ''))
        assert stats.sentence_count == 2
        assert stats.paragraph_count == 1
        assert stats.reading_time_minutes == 6 / 200  # 6 words / 200 wpm

    def test_analyze_multiple_paragraphs(self):
        """Test analysis of text with multiple paragraphs."""
        text = "First paragraph.\n\nSecond paragraph with more content."
        stats = self.analyzer.analyze(text)

        assert stats.paragraph_count == 2
        assert stats.sentence_count == 2

    def test_analyze_punctuation_handling(self):
        """Test that punctuation is handled correctly."""
        text = "Hello, world! How are you? I'm fine."
        stats = self.analyzer.analyze(text)

        # Should count words correctly despite punctuation
        assert stats.word_count == 7  # Hello, world, How, are, you, I'm, fine
        assert stats.sentence_count == 3

    def test_most_common_words(self):
        """Test most common words extraction."""
        text = "The quick brown fox jumps over the lazy dog. The fox is quick."
        stats = self.analyzer.analyze(text)

        # Should filter out stop words and short words
        common_words = [word for word, count in stats.most_common_words]
        assert "quick" in common_words
        assert "fox" in common_words
        assert "the" not in common_words  # Should be filtered out as stop word

    def test_get_words(self):
        """Test word extraction method."""
        text = "Hello, world! How are you?"
        words = self.analyzer._get_words(text)

        expected = ["hello", "world", "how", "are", "you"]
        assert words == expected

    def test_count_sentences(self):
        """Test sentence counting."""
        text = "First sentence. Second sentence! Third sentence?"
        count = self.analyzer._count_sentences(text)
        assert count == 3

    def test_count_paragraphs(self):
        """Test paragraph counting."""
        text = "First paragraph.\n\nSecond paragraph.\n\n\nThird paragraph."
        count = self.analyzer._count_paragraphs(text)
        assert count == 3

    def test_get_word_frequency(self):
        """Test word frequency calculation."""
        text = "hello world hello"
        freq = self.analyzer.get_word_frequency(text)

        assert freq["hello"] == 2
        assert freq["world"] == 1

    def test_get_reading_level_easy(self):
        """Test reading level detection for easy text."""
        text = "The cat sat. It was fun."
        level = self.analyzer.get_reading_level(text)
        assert level == "Easy"

    def test_get_reading_level_medium(self):
        """Test reading level detection for medium text."""
        text = "The sophisticated methodology employed in this research demonstrates comprehensive analytical capabilities."
        level = self.analyzer.get_reading_level(text)
        assert level in ["Medium", "Hard"]  # Could be either depending on exact calculation

    def test_get_reading_level_empty(self):
        """Test reading level detection for empty text."""
        level = self.analyzer.get_reading_level("")
        assert level == "Unknown"

    def test_reading_time_calculation(self):
        """Test reading time calculation."""
        text = "word " * 200  # 200 words
        stats = self.analyzer.analyze(text)
        assert stats.reading_time_minutes == 1.0  # 200 words / 200 wpm = 1 minute

    def test_analyze_with_special_characters(self):
        """Test analysis with special characters and unicode."""
        text = "Hello 世界! @#$%^&*()"
        stats = self.analyzer.analyze(text)

        assert stats.word_count == 2  # "Hello" and "世界"
        assert stats.character_count == len(text)

    def test_most_common_words_limit(self):
        """Test that most common words respects the limit."""
        # Create text with many repeated words
        text = " ".join(["word"] * 10 + ["another"] * 5 + ["third"] * 3 + ["single"] * 1)
        stats = self.analyzer.analyze(text)

        # Should return at most 10 words (default limit)
        assert len(stats.most_common_words) <= 10


class TestTextStats:
    """Test cases for TextStats dataclass."""

    def test_text_stats_creation(self):
        """Test TextStats object creation."""
        stats = TextStats(
            word_count=10,
            character_count=50,
            character_count_no_spaces=40,
            sentence_count=2,
            paragraph_count=1,
            reading_time_minutes=0.05,
            most_common_words=[("test", 3), ("word", 2)]
        )

        assert stats.word_count == 10
        assert stats.character_count == 50
        assert stats.character_count_no_spaces == 40
        assert stats.sentence_count == 2
        assert stats.paragraph_count == 1
        assert stats.reading_time_minutes == 0.05
        assert len(stats.most_common_words) == 2


if __name__ == "__main__":
    pytest.main([__file__])
