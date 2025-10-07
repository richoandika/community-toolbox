# QR Code Generator

A command-line tool to generate QR codes from text or URLs with various output formats and customization options.

## Features

- Generate QR codes from any text or URL
- Multiple output formats: PNG, SVG, and ASCII text
- Customizable size, border, and error correction levels
- Cross-platform compatibility

## Installation

```bash
# Install dependencies
pip install -r requirements.txt
```

## Usage

### Basic Usage

```bash
# Generate a simple QR code
python qr_generator.py "Hello World" -o hello.png

# Generate QR code for a URL
python qr_generator.py "https://example.com" -o website.png
```

### Advanced Options

```bash
# Generate SVG format
python qr_generator.py "Contact info" -o contact.svg --format svg

# Generate ASCII text representation
python qr_generator.py "Large data" -o output.txt --format txt

# Custom size and error correction
python qr_generator.py "Important data" -o important.png --size 15 --error-correction H
```

### Command Line Options

- `data`: Text or URL to encode in the QR code
- `-o, --output`: Output file path (required)
- `--format`: Output format - png, svg, or txt (default: png)
- `--size`: Size of each box in pixels (default: 10)
- `--border`: Size of the border in boxes (default: 4)
- `--error-correction`: Error correction level - L, M, Q, or H (default: M)

### Error Correction Levels

- **L (7%)**: Low - for clean environments
- **M (15%)**: Medium - default, good balance
- **Q (25%)**: Quartile - for noisy environments
- **H (30%)**: High - maximum error correction

## Examples

```bash
# Generate a QR code for a WiFi network
python qr_generator.py "WIFI:T:WPA;S:MyNetwork;P:password123;;" -o wifi.png

# Generate a QR code for contact information (vCard format)
python qr_generator.py "BEGIN:VCARD\nVERSION:3.0\nFN:John Doe\nTEL:+1234567890\nEND:VCARD" -o contact.png

# Generate a large QR code for printing
python qr_generator.py "https://github.com" -o github.png --size 20 --border 8
```

## Testing

Run the test suite:

```bash
python -m pytest tests/
```

## Requirements

- Python 3.7+
- qrcode library with PIL support

## License

MIT License - see the main project LICENSE file.
