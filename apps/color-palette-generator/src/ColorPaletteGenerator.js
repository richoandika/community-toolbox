/**
 * Color Palette Generator
 * 
 * Generates color palettes using various color theory schemes.
 */

const ColorUtils = require('./ColorUtils');

class ColorPaletteGenerator {
    constructor() {
        this.colorUtils = new ColorUtils();
    }

    /**
     * Generate a random color palette
     */
    generateRandomPalette(scheme = 'random', count = 5, seed = null) {
        if (seed) {
            this.setSeed(seed);
        }

        switch (scheme.toLowerCase()) {
            case 'complementary':
                return this.generateComplementaryPalette(count);
            case 'triadic':
                return this.generateTriadicPalette(count);
            case 'analogous':
                return this.generateAnalogousPalette(count);
            case 'monochromatic':
                return this.generateMonochromaticPalette(count);
            case 'random':
            default:
                return this.generateRandomColors(count);
        }
    }

    /**
     * Generate palette from base color
     */
    generateFromBaseColor(baseColor, scheme = 'complementary', count = 5) {
        const hex = this.colorUtils.normalizeToHex(baseColor);
        const hsl = this.colorUtils.hexToHsl(hex);
        const result = hsl.match(/\d+/g);
        const baseH = parseInt(result[0]);
        const baseS = parseInt(result[1]);
        const baseL = parseInt(result[2]);

        switch (scheme.toLowerCase()) {
            case 'complementary':
                return this.generateComplementaryFromBase(baseH, baseS, baseL, count);
            case 'triadic':
                return this.generateTriadicFromBase(baseH, baseS, baseL, count);
            case 'analogous':
                return this.generateAnalogousFromBase(baseH, baseS, baseL, count);
            case 'monochromatic':
                return this.generateMonochromaticFromBase(baseH, baseS, baseL, count);
            default:
                return this.generateRandomColors(count);
        }
    }

    /**
     * Generate complementary color palette
     */
    generateComplementaryPalette(count = 5) {
        const baseH = Math.floor(Math.random() * 360);
        const baseS = 60 + Math.floor(Math.random() * 40);
        const baseL = 40 + Math.floor(Math.random() * 40);

        return this.generateComplementaryFromBase(baseH, baseS, baseL, count);
    }

    generateComplementaryFromBase(h, s, l, count) {
        const palette = [];
        const complementaryH = (h + 180) % 360;

        // Generate variations of the base color
        for (let i = 0; i < Math.ceil(count / 2); i++) {
            const variationL = Math.max(20, Math.min(80, l + (i * 20 - 20)));
            palette.push(this.colorUtils.hslToHex(`hsl(${h}, ${s}%, ${variationL}%)`));
        }

        // Generate variations of the complementary color
        for (let i = 0; i < Math.floor(count / 2); i++) {
            const variationL = Math.max(20, Math.min(80, l + (i * 20 - 20)));
            palette.push(this.colorUtils.hslToHex(`hsl(${complementaryH}, ${s}%, ${variationL}%)`));
        }

        return palette.slice(0, count);
    }

    /**
     * Generate triadic color palette
     */
    generateTriadicPalette(count = 5) {
        const baseH = Math.floor(Math.random() * 360);
        const baseS = 60 + Math.floor(Math.random() * 40);
        const baseL = 40 + Math.floor(Math.random() * 40);

        return this.generateTriadicFromBase(baseH, baseS, baseL, count);
    }

    generateTriadicFromBase(h, s, l, count) {
        const palette = [];
        const triadic1 = (h + 120) % 360;
        const triadic2 = (h + 240) % 360;

        const hues = [h, triadic1, triadic2];
        
        for (let i = 0; i < count; i++) {
            const hueIndex = i % hues.length;
            const lightness = Math.max(20, Math.min(80, l + (Math.floor(i / hues.length) * 20 - 20)));
            palette.push(this.colorUtils.hslToHex(`hsl(${hues[hueIndex]}, ${s}%, ${lightness}%)`));
        }

        return palette;
    }

    /**
     * Generate analogous color palette
     */
    generateAnalogousPalette(count = 5) {
        const baseH = Math.floor(Math.random() * 360);
        const baseS = 60 + Math.floor(Math.random() * 40);
        const baseL = 40 + Math.floor(Math.random() * 40);

        return this.generateAnalogousFromBase(baseH, baseS, baseL, count);
    }

    generateAnalogousFromBase(h, s, l, count) {
        const palette = [];
        const step = 30; // Degrees between analogous colors

        for (let i = 0; i < count; i++) {
            const hue = (h + (i * step - (count - 1) * step / 2) + 360) % 360;
            const lightness = Math.max(20, Math.min(80, l + (i * 10 - (count - 1) * 5)));
            palette.push(this.colorUtils.hslToHex(`hsl(${hue}, ${s}%, ${lightness}%)`));
        }

        return palette;
    }

    /**
     * Generate monochromatic color palette
     */
    generateMonochromaticPalette(count = 5) {
        const baseH = Math.floor(Math.random() * 360);
        const baseS = 60 + Math.floor(Math.random() * 40);
        const baseL = 40 + Math.floor(Math.random() * 40);

        return this.generateMonochromaticFromBase(baseH, baseS, baseL, count);
    }

    generateMonochromaticFromBase(h, s, l, count) {
        const palette = [];
        const step = 60 / (count - 1);

        for (let i = 0; i < count; i++) {
            const lightness = Math.max(10, Math.min(90, l + (i * step - 30)));
            palette.push(this.colorUtils.hslToHex(`hsl(${h}, ${s}%, ${lightness}%)`));
        }

        return palette;
    }

    /**
     * Generate completely random colors
     */
    generateRandomColors(count = 5) {
        const palette = [];
        for (let i = 0; i < count; i++) {
            palette.push(this.colorUtils.generateRandomHex());
        }
        return palette;
    }

    /**
     * Generate warm color palette
     */
    generateWarmPalette(count = 5) {
        const palette = [];
        const warmHues = [0, 15, 30, 45, 60]; // Red, orange, yellow range

        for (let i = 0; i < count; i++) {
            const hue = warmHues[i % warmHues.length] + Math.floor(Math.random() * 15);
            const saturation = 60 + Math.floor(Math.random() * 40);
            const lightness = 40 + Math.floor(Math.random() * 40);
            palette.push(this.colorUtils.hslToHex(`hsl(${hue}, ${saturation}%, ${lightness}%)`));
        }

        return palette;
    }

    /**
     * Generate cool color palette
     */
    generateCoolPalette(count = 5) {
        const palette = [];
        const coolHues = [180, 195, 210, 225, 240]; // Cyan, blue range

        for (let i = 0; i < count; i++) {
            const hue = coolHues[i % coolHues.length] + Math.floor(Math.random() * 15);
            const saturation = 60 + Math.floor(Math.random() * 40);
            const lightness = 40 + Math.floor(Math.random() * 40);
            palette.push(this.colorUtils.hslToHex(`hsl(${hue}, ${saturation}%, ${lightness}%)`));
        }

        return palette;
    }

    /**
     * Generate pastel color palette
     */
    generatePastelPalette(count = 5) {
        const palette = [];
        
        for (let i = 0; i < count; i++) {
            const hue = Math.floor(Math.random() * 360);
            const saturation = 20 + Math.floor(Math.random() * 30); // Low saturation
            const lightness = 70 + Math.floor(Math.random() * 20); // High lightness
            palette.push(this.colorUtils.hslToHex(`hsl(${hue}, ${saturation}%, ${lightness}%)`));
        }

        return palette;
    }

    /**
     * Generate vibrant color palette
     */
    generateVibrantPalette(count = 5) {
        const palette = [];
        
        for (let i = 0; i < count; i++) {
            const hue = Math.floor(Math.random() * 360);
            const saturation = 80 + Math.floor(Math.random() * 20); // High saturation
            const lightness = 40 + Math.floor(Math.random() * 20); // Medium lightness
            palette.push(this.colorUtils.hslToHex(`hsl(${hue}, ${saturation}%, ${lightness}%)`));
        }

        return palette;
    }

    /**
     * Set random seed for reproducible results
     */
    setSeed(seed) {
        // Simple linear congruential generator
        this.seed = seed;
        this.random = () => {
            this.seed = (this.seed * 1664525 + 1013904223) % Math.pow(2, 32);
            return this.seed / Math.pow(2, 32);
        };
    }

    /**
     * Get color palette information
     */
    getPaletteInfo(palette) {
        const info = {
            count: palette.length,
            colors: palette,
            formats: {
                hex: palette,
                rgb: palette.map(color => this.colorUtils.hexToRgb(color)),
                hsl: palette.map(color => this.colorUtils.hexToHsl(color))
            },
            brightness: palette.map(color => this.colorUtils.getBrightness(color)),
            isLight: palette.map(color => this.colorUtils.isLight(color))
        };

        return info;
    }
}

module.exports = ColorPaletteGenerator;
