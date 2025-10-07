# Color Palette Generator (Node.js)

A comprehensive utility for generating and manipulating color palettes using various color theory schemes. Perfect for designers, developers, and anyone working with colors.

## Features

- **Multiple Color Schemes**: Complementary, triadic, analogous, monochromatic, and random palettes
- **Color Format Support**: Generate palettes in HEX, RGB, and HSL formats
- **Base Color Input**: Create palettes from any base color in multiple formats
- **Specialized Palettes**: Warm, cool, pastel, and vibrant color collections
- **Color Analysis**: Brightness calculation, contrast detection, and color variations
- **Multiple Output Formats**: Console display, JSON export, and CSS generation
- **Reproducible Results**: Seed-based generation for consistent results

## Installation

```bash
# Install dependencies
npm install

# Run tests
npm test
```

## Usage

### Command Line Interface

```bash
# Generate a random complementary palette
node index.js --scheme complementary --count 6

# Generate palette from base color
node index.js --base "#ff0000" --scheme triadic --format rgb

# Generate pastel palette and save to file
node index.js --scheme random --count 8 --output json --file palette.json

# Generate CSS variables
node index.js --scheme analogous --count 5 --output css --file colors.css
```

### Command Line Options

| Option | Short | Description | Default |
|--------|-------|-------------|---------|
| `--scheme` | `-s` | Color scheme (complementary, triadic, analogous, monochromatic, random) | `complementary` |
| `--count` | `-c` | Number of colors in palette | `5` |
| `--base` | `-b` | Base color (hex, rgb, or hsl format) | Random |
| `--format` | `-f` | Output format (hex, rgb, hsl, css) | `hex` |
| `--output` | `-o` | Output type (console, json, css) | `console` |
| `--file` | | Save palette to file | |
| `--seed` | | Seed for reproducible generation | |
| `--help` | `-h` | Show help message | |
| `--version` | `-v` | Show version number | |

### Programmatic Usage

```javascript
const ColorPaletteGenerator = require('./src/ColorPaletteGenerator');
const ColorUtils = require('./src/ColorUtils');

// Create generator instance
const generator = new ColorPaletteGenerator();
const colorUtils = new ColorUtils();

// Generate random palette
const randomPalette = generator.generateRandomPalette('complementary', 5);
console.log(randomPalette);

// Generate from base color
const basePalette = generator.generateFromBaseColor('#ff0000', 'triadic', 6);
console.log(basePalette);

// Generate specialized palettes
const warmPalette = generator.generateWarmPalette(5);
const coolPalette = generator.generateCoolPalette(5);
const pastelPalette = generator.generatePastelPalette(5);
const vibrantPalette = generator.generateVibrantPalette(5);

// Get palette information
const info = generator.getPaletteInfo(basePalette);
console.log(info);
```

## Color Schemes

### Complementary
Colors that are opposite each other on the color wheel, creating high contrast.

```bash
node index.js --scheme complementary --count 4
```

### Triadic
Three colors evenly spaced around the color wheel, creating vibrant combinations.

```bash
node index.js --scheme triadic --count 6
```

### Analogous
Colors that are adjacent to each other on the color wheel, creating harmonious palettes.

```bash
node index.js --scheme analogous --count 5
```

### Monochromatic
Different shades and tints of a single color, creating subtle variations.

```bash
node index.js --scheme monochromatic --count 5
```

### Specialized Palettes

```javascript
// Warm colors (reds, oranges, yellows)
const warmPalette = generator.generateWarmPalette(5);

// Cool colors (blues, cyans, purples)
const coolPalette = generator.generateCoolPalette(5);

// Pastel colors (light, soft colors)
const pastelPalette = generator.generatePastelPalette(5);

// Vibrant colors (high saturation)
const vibrantPalette = generator.generateVibrantPalette(5);
```

## Color Utilities

```javascript
const colorUtils = new ColorUtils();

// Color conversion
const rgb = colorUtils.hexToRgb('#ff0000');        // "rgb(255, 0, 0)"
const hsl = colorUtils.hexToHsl('#ff0000');        // "hsl(0, 100%, 50%)"
const hex = colorUtils.rgbToHex('rgb(255, 0, 0)'); // "#ff0000"

// Color analysis
const brightness = colorUtils.getBrightness('#ff0000');     // 76
const isLight = colorUtils.isLight('#ff0000');             // false
const contrast = colorUtils.getContrastColor('#ff0000');   // "#ffffff"

// Color manipulation
const brighter = colorUtils.adjustBrightness('#808080', 50);
const variations = colorUtils.generateVariations('#ff0000', 5);

// Color validation
const isValid = colorUtils.isValidColor('#ff0000');        // true
const normalized = colorUtils.normalizeToHex('rgb(255, 0, 0)'); // "#ff0000"
```

## Output Formats

### Console Output
```
🎨 Color Palette (complementary scheme, 5 colors)

1. #ff6b6b
2. #4ecdc4
3. #45b7d1
4. #96ceb4
5. #feca57

📋 Copy-paste ready:
#ff6b6b, #4ecdc4, #45b7d1, #96ceb4, #feca57
```

### JSON Output
```json
{
  "scheme": "complementary",
  "count": 5,
  "colors": ["#ff6b6b", "#4ecdc4", "#45b7d1", "#96ceb4", "#feca57"],
  "generated": "2024-01-15T10:30:00.000Z"
}
```

### CSS Output
```css
:root {
  --color-1: #ff6b6b;
  --color-2: #4ecdc4;
  --color-3: #45b7d1;
  --color-4: #96ceb4;
  --color-5: #feca57;
}

.color-palette {
  .color-1 { background-color: #ff6b6b; }
  .color-2 { background-color: #4ecdc4; }
  .color-3 { background-color: #45b7d1; }
  .color-4 { background-color: #96ceb4; }
  .color-5 { background-color: #feca57; }
}
```

## Examples

### Design Workflow
```bash
# Generate a brand color palette
node index.js --base "#2c3e50" --scheme triadic --count 6 --output css --file brand-colors.css

# Create a UI component palette
node index.js --scheme analogous --count 8 --format rgb --output json --file ui-palette.json

# Generate accessible color variations
node index.js --base "#3498db" --scheme monochromatic --count 7 --format hsl
```

### Development Integration
```javascript
// Generate colors for a chart library
const chartColors = generator.generateRandomPalette('random', 10);

// Create a theme system
const themeColors = generator.generateFromBaseColor('#6366f1', 'analogous', 5);
const themeInfo = generator.getPaletteInfo(themeColors);

// Export for CSS-in-JS
const cssVars = themeColors.map((color, index) => 
  `--theme-color-${index + 1}: ${color};`
).join('\n');
```

## API Reference

### ColorPaletteGenerator

#### Methods
- `generateRandomPalette(scheme, count, seed)` - Generate random palette
- `generateFromBaseColor(baseColor, scheme, count)` - Generate from base color
- `generateComplementaryPalette(count)` - Generate complementary palette
- `generateTriadicPalette(count)` - Generate triadic palette
- `generateAnalogousPalette(count)` - Generate analogous palette
- `generateMonochromaticPalette(count)` - Generate monochromatic palette
- `generateWarmPalette(count)` - Generate warm color palette
- `generateCoolPalette(count)` - Generate cool color palette
- `generatePastelPalette(count)` - Generate pastel color palette
- `generateVibrantPalette(count)` - Generate vibrant color palette
- `getPaletteInfo(palette)` - Get comprehensive palette information

### ColorUtils

#### Methods
- `hexToRgb(hex)` - Convert hex to RGB
- `rgbToHex(rgb)` - Convert RGB to hex
- `hexToHsl(hex)` - Convert hex to HSL
- `hslToHex(hsl)` - Convert HSL to hex
- `isValidColor(color)` - Validate color format
- `normalizeToHex(color)` - Normalize color to hex
- `getBrightness(hex)` - Get color brightness
- `isLight(hex)` - Check if color is light
- `getContrastColor(hex)` - Get contrasting color
- `adjustBrightness(hex, percent)` - Adjust color brightness
- `generateVariations(baseColor, count)` - Generate color variations

## Running Tests

```bash
# Run all tests
npm test

# Run tests in watch mode
npm run test:watch

# Run specific test file
npm test ColorUtils.test.js
```

## Requirements

- Node.js 14.0.0 or higher
- No external dependencies (uses only standard library)

## Contributing

This tool is part of the Community Toolbox project. Feel free to contribute improvements, additional color schemes, or new features following the project's contribution guidelines.

## License

This project is licensed under the terms of the [MIT License](../../LICENSE).
