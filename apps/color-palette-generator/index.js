#!/usr/bin/env node

/**
 * Color Palette Generator
 * 
 * A comprehensive utility for generating and manipulating color palettes
 * with various color schemes and output formats.
 */

const ColorPaletteGenerator = require('./src/ColorPaletteGenerator');
const ColorUtils = require('./src/ColorUtils');

class ColorPaletteCLI {
    constructor() {
        this.generator = new ColorPaletteGenerator();
        this.colorUtils = new ColorUtils();
    }

    /**
     * Parse command line arguments
     */
    parseArgs() {
        const args = process.argv.slice(2);
        const options = {
            scheme: 'complementary',
            count: 5,
            baseColor: null,
            format: 'hex',
            output: 'console',
            file: null,
            seed: null
        };

        for (let i = 0; i < args.length; i++) {
            const arg = args[i];
            
            switch (arg) {
                case '--scheme':
                case '-s':
                    options.scheme = args[++i];
                    break;
                case '--count':
                case '-c':
                    options.count = parseInt(args[++i]) || 5;
                    break;
                case '--base':
                case '-b':
                    options.baseColor = args[++i];
                    break;
                case '--format':
                case '-f':
                    options.format = args[++i];
                    break;
                case '--output':
                case '-o':
                    options.output = args[++i];
                    break;
                case '--file':
                    options.file = args[++i];
                    break;
                case '--seed':
                    options.seed = args[++i];
                    break;
                case '--help':
                case '-h':
                    this.showHelp();
                    process.exit(0);
                    break;
                case '--version':
                case '-v':
                    console.log('Color Palette Generator v1.0.0');
                    process.exit(0);
                    break;
            }
        }

        return options;
    }

    /**
     * Show help information
     */
    showHelp() {
        console.log(`
Color Palette Generator v1.0.0

Usage: node index.js [options]

Options:
  -s, --scheme <type>     Color scheme type (complementary, triadic, analogous, monochromatic, random)
  -c, --count <number>     Number of colors in palette (default: 5)
  -b, --base <color>       Base color (hex, rgb, or hsl format)
  -f, --format <type>      Output format (hex, rgb, hsl, css) (default: hex)
  -o, --output <type>      Output type (console, json, css) (default: console)
  --file <path>           Save palette to file
  --seed <value>          Seed for random generation
  -h, --help              Show this help message
  -v, --version           Show version number

Examples:
  node index.js --scheme complementary --count 6
  node index.js --base "#ff0000" --scheme triadic --format rgb
  node index.js --scheme random --count 8 --output json --file palette.json
        `);
    }

    /**
     * Generate and display palette
     */
    async generatePalette(options) {
        try {
            let palette;
            
            if (options.baseColor) {
                // Validate base color
                if (!this.colorUtils.isValidColor(options.baseColor)) {
                    throw new Error(`Invalid base color: ${options.baseColor}`);
                }
                palette = this.generator.generateFromBaseColor(
                    options.baseColor, 
                    options.scheme, 
                    options.count
                );
            } else {
                palette = this.generator.generateRandomPalette(
                    options.scheme, 
                    options.count, 
                    options.seed
                );
            }

            // Convert to requested format
            const formattedPalette = this.formatPalette(palette, options.format);

            // Output palette
            await this.outputPalette(formattedPalette, options);

        } catch (error) {
            console.error('Error generating palette:', error.message);
            process.exit(1);
        }
    }

    /**
     * Format palette to requested format
     */
    formatPalette(palette, format) {
        return palette.map(color => {
            switch (format.toLowerCase()) {
                case 'rgb':
                    return this.colorUtils.hexToRgb(color);
                case 'hsl':
                    return this.colorUtils.hexToHsl(color);
                case 'css':
                    return `color: ${color};`;
                default:
                    return color;
            }
        });
    }

    /**
     * Output palette in requested format
     */
    async outputPalette(palette, options) {
        const fs = require('fs').promises;

        switch (options.output.toLowerCase()) {
            case 'json':
                const jsonOutput = JSON.stringify({
                    scheme: options.scheme,
                    count: palette.length,
                    colors: palette,
                    generated: new Date().toISOString()
                }, null, 2);
                
                if (options.file) {
                    await fs.writeFile(options.file, jsonOutput);
                    console.log(`Palette saved to ${options.file}`);
                } else {
                    console.log(jsonOutput);
                }
                break;

            case 'css':
                const cssOutput = this.generateCSS(palette);
                if (options.file) {
                    await fs.writeFile(options.file, cssOutput);
                    console.log(`CSS saved to ${options.file}`);
                } else {
                    console.log(cssOutput);
                }
                break;

            default:
                this.displayConsole(palette, options);
        }
    }

    /**
     * Generate CSS output
     */
    generateCSS(palette) {
        let css = ':root {\n';
        palette.forEach((color, index) => {
            css += `  --color-${index + 1}: ${color};\n`;
        });
        css += '}\n\n';
        
        css += '.color-palette {\n';
        palette.forEach((color, index) => {
            css += `  .color-${index + 1} { background-color: ${color}; }\n`;
        });
        css += '}';
        
        return css;
    }

    /**
     * Display palette in console
     */
    displayConsole(palette, options) {
        console.log(`\n🎨 Color Palette (${options.scheme} scheme, ${palette.length} colors)\n`);
        
        palette.forEach((color, index) => {
            const colorInfo = this.getColorInfo(color, options.format);
            console.log(`${index + 1}. ${colorInfo}`);
        });
        
        console.log('\n📋 Copy-paste ready:');
        console.log(palette.join(', '));
    }

    /**
     * Get formatted color information
     */
    getColorInfo(color, format) {
        switch (format.toLowerCase()) {
            case 'rgb':
                return `${color} (RGB: ${this.colorUtils.hexToRgb(color)})`;
            case 'hsl':
                return `${color} (HSL: ${this.colorUtils.hexToHsl(color)})`;
            default:
                return color;
        }
    }

    /**
     * Main execution method
     */
    async run() {
        const options = this.parseArgs();
        await this.generatePalette(options);
    }
}

// Run CLI if this file is executed directly
if (require.main === module) {
    const cli = new ColorPaletteCLI();
    cli.run().catch(error => {
        console.error('Fatal error:', error.message);
        process.exit(1);
    });
}

module.exports = ColorPaletteCLI;
