# Morse Code Translator (Python)

A lightweight Morse code translator that converts plain text to International
Morse code and back again. The utility ships with a dependency-free Python
module and a command-line interface so it can be used in scripts or directly
from the terminal.

## Features

- **Bidirectional translation** – encode text as Morse code or decode Morse
  code back to readable text
- **Flexible separators** – customise the separator used for letters and words
- **Extensive alphabet** – supports letters, numbers, and common punctuation
- **CLI friendly** – translate without writing a single line of Python

## Usage

### Python API

```python
from apps.morse_code_translator import encode_to_morse, decode_from_morse

encoded = encode_to_morse("Hello World")
print(encoded)  # .... . .-.. .-.. --- / .-- --- .-. .-.. -..

print(decode_from_morse(encoded))  # HELLO WORLD
```

### Command Line Interface

```bash
# Encode text to Morse code
python -m apps.morse_code_translator.morse_translator --text "sos"

# Decode Morse code back into text
python -m apps.morse_code_translator.morse_translator --morse "... --- ..."

# Custom separators
python -m apps.morse_code_translator.morse_translator --text "help" --letter-sep "|" --word-sep "/"
```

## Running Tests

```bash
python -m pytest apps/morse_code_translator
```

## Requirements

- Python 3.9+
- No external dependencies

## License

This project is released under the MIT License as part of the Community
Toolbox repository.
