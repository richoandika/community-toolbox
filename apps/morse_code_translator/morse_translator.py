"""Command-line Morse code translator.

This module provides utility functions for converting between plain text and
International Morse code. It also exposes a small CLI so the translator can be
used from the command line without any extra dependencies.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass
from typing import Dict, Iterable, List

# International Morse code reference for alphanumeric characters and common
# punctuation marks. " " (space) is handled separately at runtime.
MORSE_CODE_TABLE: Dict[str, str] = {
    "A": ".-",
    "B": "-...",
    "C": "-.-.",
    "D": "-..",
    "E": ".",
    "F": "..-.",
    "G": "--.",
    "H": "....",
    "I": "..",
    "J": ".---",
    "K": "-.-",
    "L": ".-..",
    "M": "--",
    "N": "-.",
    "O": "---",
    "P": ".--.",
    "Q": "--.-",
    "R": ".-.",
    "S": "...",
    "T": "-",
    "U": "..-",
    "V": "...-",
    "W": ".--",
    "X": "-..-",
    "Y": "-.--",
    "Z": "--..",
    "0": "-----",
    "1": ".----",
    "2": "..---",
    "3": "...--",
    "4": "....-",
    "5": ".....",
    "6": "-....",
    "7": "--...",
    "8": "---..",
    "9": "----.",
    ".": ".-.-.-",
    ",": "--..--",
    "?": "..--..",
    "'": ".----.",
    "!": "-.-.--",
    "/": "-..-.",
    "(": "-.--.",
    ")": "-.--.-",
    "&": ".-...",
    ":": "---...",
    ";": "-.-.-.",
    "=": "-...-",
    "+": ".-.-.",
    "-": "-....-",
    "_": "..--.-",
    "\"": ".-..-.",
    "$": "...-..-",
    "@": ".--.-.",
}

REVERSE_MORSE_CODE_TABLE: Dict[str, str] = {value: key for key, value in MORSE_CODE_TABLE.items()}

DEFAULT_LETTER_SEPARATOR = " "
DEFAULT_WORD_SEPARATOR = " / "


@dataclass
class TranslationResult:
    """Representation of a translation and the source of the transformation."""

    source: str
    translated: str


def _normalize_text(text: str) -> Iterable[str]:
    """Yield characters for encoding after normalising the input text."""

    for character in text:
        if character == " ":
            yield character
        else:
            yield character.upper()


def encode_to_morse(text: str, *, letter_sep: str = DEFAULT_LETTER_SEPARATOR, word_sep: str = DEFAULT_WORD_SEPARATOR) -> str:
    """Convert plain text to Morse code.

    Unknown characters raise a :class:`ValueError` so callers can decide how to
    handle unsupported input explicitly.
    """

    words: List[str] = []
    current_letters: List[str] = []

    for character in _normalize_text(text):
        if character == " ":
            if current_letters:
                words.append(letter_sep.join(current_letters))
                current_letters = []
            continue

        try:
            current_letters.append(MORSE_CODE_TABLE[character])
        except KeyError as exc:  # pragma: no cover - defensive but difficult to hit
            raise ValueError(f"Unsupported character for Morse code: {character!r}") from exc

    if current_letters:
        words.append(letter_sep.join(current_letters))

    return word_sep.join(words)


def decode_from_morse(morse: str, *, letter_sep: str = DEFAULT_LETTER_SEPARATOR, word_sep: str = DEFAULT_WORD_SEPARATOR) -> str:
    """Convert Morse code back into human-readable text."""

    if not morse.strip():
        return ""

    decoded_words: List[str] = []
    for raw_word in morse.split(word_sep):
        stripped_word = raw_word.strip()
        if not stripped_word:
            continue

        decoded_letters: List[str] = []
        for token in filter(None, stripped_word.split(letter_sep)):
            try:
                decoded_letters.append(REVERSE_MORSE_CODE_TABLE[token])
            except KeyError as exc:
                raise ValueError(f"Unsupported Morse sequence: {token!r}") from exc

        decoded_words.append("".join(decoded_letters))

    return " ".join(decoded_words)


def build_argument_parser() -> argparse.ArgumentParser:
    """Create the argument parser used by the CLI entry point."""

    parser = argparse.ArgumentParser(description="Translate text to and from Morse code.")
    parser.add_argument(
        "--letter-sep",
        default=DEFAULT_LETTER_SEPARATOR,
        help="Separator to use between individual Morse letters (default: space)",
    )
    parser.add_argument(
        "--word-sep",
        default=DEFAULT_WORD_SEPARATOR,
        help="Separator to use between Morse words (default: ' / ')",
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--text", help="Plain text to convert into Morse code")
    group.add_argument("--morse", help="Morse code to convert back into text")
    return parser


def main(argv: Iterable[str] | None = None) -> TranslationResult:
    """Entry point that powers the command line interface."""

    parser = build_argument_parser()
    args = parser.parse_args(list(argv) if argv is not None else None)

    if args.text is not None:
        translation = encode_to_morse(args.text, letter_sep=args.letter_sep, word_sep=args.word_sep)
        return TranslationResult(source=args.text, translated=translation)

    translation = decode_from_morse(args.morse, letter_sep=args.letter_sep, word_sep=args.word_sep)
    return TranslationResult(source=args.morse, translated=translation)


if __name__ == "__main__":  # pragma: no cover - CLI execution path
    result = main()
    print(result.translated)
