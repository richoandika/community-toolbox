import subprocess
import sys

import pytest

from apps.morse_code_translator import decode_from_morse, encode_to_morse


@pytest.mark.parametrize(
    "text, expected",
    [
        ("SOS", "... --- ..."),
        ("Hello World", ".... . .-.. .-.. --- / .-- --- .-. .-.. -.."),
        ("2024", "..--- ----- ..--- ....-"),
    ],
)
def test_encode_to_morse(text, expected):
    assert encode_to_morse(text) == expected


def test_decode_from_morse():
    assert decode_from_morse(".... . .-.. .-.. ---") == "HELLO"


@pytest.mark.parametrize(
    "text",
    ["Community Toolbox", "Python 3.11", "Test-driven development!"],
)
def test_round_trip(text):
    encoded = encode_to_morse(text)
    decoded = decode_from_morse(encoded)
    # Numbers and punctuation are normalised to uppercase in Morse code translations.
    assert decoded == text.upper()


def test_decode_invalid_sequence():
    with pytest.raises(ValueError):
        decode_from_morse(".-.-.-.-")


def test_cli_encode(tmp_path):
    script = "from apps.morse_code_translator.morse_translator import main; print(main(['--text', 'abc']).translated)"
    result = subprocess.run([sys.executable, "-c", script], check=True, capture_output=True, text=True)
    assert result.stdout.strip() == ".- -... -.-."
