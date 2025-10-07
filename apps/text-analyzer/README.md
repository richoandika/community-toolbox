# Text Analyzer (Python)

A comprehensive text analysis utility that provides detailed statistics about text content including word count, character count, reading time estimation, and text complexity analysis.

## Features

- **Word and Character Counting**: Count total words, characters (with and without spaces)
- **Reading Time Estimation**: Calculate estimated reading time based on average reading speed
- **Text Structure Analysis**: Count sentences and paragraphs
- **Reading Level Assessment**: Determine if text is Easy, Medium, or Hard to read
- **Word Frequency Analysis**: Find most common words in the text
- **Stop Word Filtering**: Automatically filters out common words for better analysis

## Usage

### As a Python Module

```python
from apps.text_analyzer import TextAnalyzer

analyzer = TextAnalyzer()
stats = analyzer.analyze("Your text here...")

print(f"Word count: {stats.word_count}")
print(f"Reading time: {stats.reading_time_minutes:.1f} minutes")
print(f"Reading level: {analyzer.get_reading_level('Your text here...')}")
```

### Command Line Interface

```bash
# Analyze text from a file
python text_analyzer.py sample.txt

# Analyze text directly
python text_analyzer.py --text "Your text content here"
```

### Example Output

```
=== Text Analysis Results ===
Word count: 150
Character count: 850
Character count (no spaces): 750
Sentence count: 8
Paragraph count: 3
Reading time: 0.8 minutes
Reading level: Medium

Most common words:
  text: 5
  analysis: 3
  content: 2
```

## API Reference

### TextAnalyzer Class

#### Methods

- `analyze(text: str) -> TextStats`: Analyze text and return comprehensive statistics
- `get_word_frequency(text: str) -> Dict[str, int]`: Get frequency count for all words
- `get_reading_level(text: str) -> str`: Estimate reading difficulty level

### TextStats Dataclass

Contains the following attributes:
- `word_count`: Number of words in the text
- `character_count`: Total character count
- `character_count_no_spaces`: Character count excluding spaces
- `sentence_count`: Number of sentences
- `paragraph_count`: Number of paragraphs
- `reading_time_minutes`: Estimated reading time in minutes
- `most_common_words`: List of tuples (word, frequency) for most common words

## Running Tests

```bash
# Run tests with pytest
python -m pytest apps/text-analyzer

# Run tests with verbose output
python -m pytest apps/text-analyzer -v

# Run specific test file
python -m pytest apps/text-analyzer/tests/test_text_analyzer.py
```

## Requirements

- Python 3.6+
- No external dependencies (uses only standard library)

## Examples

### Basic Text Analysis

```python
from apps.text_analyzer import TextAnalyzer

analyzer = TextAnalyzer()
text = "The quick brown fox jumps over the lazy dog. This is a sample text for analysis."

stats = analyzer.analyze(text)
print(f"Words: {stats.word_count}")
print(f"Sentences: {stats.sentence_count}")
print(f"Reading time: {stats.reading_time_minutes:.1f} minutes")
```

### Word Frequency Analysis

```python
freq = analyzer.get_word_frequency("hello world hello")
print(freq)  # {'hello': 2, 'world': 1}
```

### Reading Level Assessment

```python
easy_text = "The cat sat on the mat."
hard_text = "The sophisticated methodology employed demonstrates comprehensive analytical capabilities."

print(analyzer.get_reading_level(easy_text))  # "Easy"
print(analyzer.get_reading_level(hard_text))  # "Hard"
```

## Contributing

This tool is part of the Community Toolbox project. Feel free to contribute improvements, additional features, or bug fixes following the project's contribution guidelines.
