/**
 * Tests for ColorUtils class
 */

const ColorUtils = require('../src/ColorUtils');

describe('ColorUtils', () => {
    let colorUtils;

    beforeEach(() => {
        colorUtils = new ColorUtils();
    });

    describe('hexToRgb', () => {
        test('should convert hex to RGB correctly', () => {
            expect(colorUtils.hexToRgb('#ff0000')).toBe('rgb(255, 0, 0)');
            expect(colorUtils.hexToRgb('#00ff00')).toBe('rgb(0, 255, 0)');
            expect(colorUtils.hexToRgb('#0000ff')).toBe('rgb(0, 0, 255)');
            expect(colorUtils.hexToRgb('#ffffff')).toBe('rgb(255, 255, 255)');
            expect(colorUtils.hexToRgb('#000000')).toBe('rgb(0, 0, 0)');
        });

        test('should handle hex without #', () => {
            expect(colorUtils.hexToRgb('ff0000')).toBe('rgb(255, 0, 0)');
        });

        test('should throw error for invalid hex', () => {
            expect(() => colorUtils.hexToRgb('invalid')).toThrow('Invalid hex color');
            expect(() => colorUtils.hexToRgb('#gg0000')).toThrow('Invalid hex color');
        });
    });

    describe('rgbToHex', () => {
        test('should convert RGB to hex correctly', () => {
            expect(colorUtils.rgbToHex('rgb(255, 0, 0)')).toBe('#ff0000');
            expect(colorUtils.rgbToHex('rgb(0, 255, 0)')).toBe('#00ff00');
            expect(colorUtils.rgbToHex('rgb(0, 0, 255)')).toBe('#0000ff');
            expect(colorUtils.rgbToHex('rgb(255, 255, 255)')).toBe('#ffffff');
            expect(colorUtils.rgbToHex('rgb(0, 0, 0)')).toBe('#000000');
        });

        test('should throw error for invalid RGB', () => {
            expect(() => colorUtils.rgbToHex('invalid')).toThrow('Invalid RGB color');
            expect(() => colorUtils.rgbToHex('rgb(256, 0, 0)')).toThrow('Invalid RGB color');
        });
    });

    describe('hexToHsl', () => {
        test('should convert hex to HSL correctly', () => {
            const red = colorUtils.hexToHsl('#ff0000');
            expect(red).toMatch(/hsl\(0, 100%, 50%\)/);
            
            const green = colorUtils.hexToHsl('#00ff00');
            expect(green).toMatch(/hsl\(120, 100%, 50%\)/);
            
            const blue = colorUtils.hexToHsl('#0000ff');
            expect(blue).toMatch(/hsl\(240, 100%, 50%\)/);
        });
    });

    describe('hslToHex', () => {
        test('should convert HSL to hex correctly', () => {
            expect(colorUtils.hslToHex('hsl(0, 100%, 50%)')).toBe('#ff0000');
            expect(colorUtils.hslToHex('hsl(120, 100%, 50%)')).toBe('#00ff00');
            expect(colorUtils.hslToHex('hsl(240, 100%, 50%)')).toBe('#0000ff');
        });

        test('should throw error for invalid HSL', () => {
            expect(() => colorUtils.hslToHex('invalid')).toThrow('Invalid HSL color');
        });
    });

    describe('isValidColor', () => {
        test('should validate hex colors', () => {
            expect(colorUtils.isValidColor('#ff0000')).toBe(true);
            expect(colorUtils.isValidColor('ff0000')).toBe(true);
            expect(colorUtils.isValidColor('#gg0000')).toBe(false);
        });

        test('should validate RGB colors', () => {
            expect(colorUtils.isValidColor('rgb(255, 0, 0)')).toBe(true);
            expect(colorUtils.isValidColor('rgb(256, 0, 0)')).toBe(false);
        });

        test('should validate HSL colors', () => {
            expect(colorUtils.isValidColor('hsl(0, 100%, 50%)')).toBe(true);
            expect(colorUtils.isValidColor('hsl(0, 101%, 50%)')).toBe(false);
        });

        test('should return false for invalid inputs', () => {
            expect(colorUtils.isValidColor('')).toBe(false);
            expect(colorUtils.isValidColor(null)).toBe(false);
            expect(colorUtils.isValidColor(undefined)).toBe(false);
            expect(colorUtils.isValidColor(123)).toBe(false);
        });
    });

    describe('normalizeToHex', () => {
        test('should normalize hex colors', () => {
            expect(colorUtils.normalizeToHex('#ff0000')).toBe('#ff0000');
            expect(colorUtils.normalizeToHex('ff0000')).toBe('#ff0000');
        });

        test('should normalize RGB colors', () => {
            expect(colorUtils.normalizeToHex('rgb(255, 0, 0)')).toBe('#ff0000');
        });

        test('should normalize HSL colors', () => {
            expect(colorUtils.normalizeToHex('hsl(0, 100%, 50%)')).toBe('#ff0000');
        });

        test('should throw error for invalid colors', () => {
            expect(() => colorUtils.normalizeToHex('invalid')).toThrow('Invalid color format');
        });
    });

    describe('generateRandomHex', () => {
        test('should generate valid hex colors', () => {
            const color = colorUtils.generateRandomHex();
            expect(color).toMatch(/^#[0-9a-f]{6}$/);
            expect(colorUtils.isValidColor(color)).toBe(true);
        });
    });

    describe('getBrightness', () => {
        test('should calculate brightness correctly', () => {
            expect(colorUtils.getBrightness('#ffffff')).toBe(255);
            expect(colorUtils.getBrightness('#000000')).toBe(0);
            expect(colorUtils.getBrightness('#808080')).toBe(128);
        });
    });

    describe('isLight', () => {
        test('should identify light colors', () => {
            expect(colorUtils.isLight('#ffffff')).toBe(true);
            expect(colorUtils.isLight('#ffff00')).toBe(true);
            expect(colorUtils.isLight('#000000')).toBe(false);
            expect(colorUtils.isLight('#0000ff')).toBe(false);
        });
    });

    describe('getContrastColor', () => {
        test('should return black for light colors', () => {
            expect(colorUtils.getContrastColor('#ffffff')).toBe('#000000');
            expect(colorUtils.getContrastColor('#ffff00')).toBe('#000000');
        });

        test('should return white for dark colors', () => {
            expect(colorUtils.getContrastColor('#000000')).toBe('#ffffff');
            expect(colorUtils.getContrastColor('#0000ff')).toBe('#ffffff');
        });
    });

    describe('adjustBrightness', () => {
        test('should increase brightness', () => {
            const result = colorUtils.adjustBrightness('#808080', 50);
            expect(colorUtils.getBrightness(result)).toBeGreaterThan(128);
        });

        test('should decrease brightness', () => {
            const result = colorUtils.adjustBrightness('#808080', -50);
            expect(colorUtils.getBrightness(result)).toBeLessThan(128);
        });

        test('should clamp values', () => {
            const result = colorUtils.adjustBrightness('#000000', 200);
            expect(colorUtils.getBrightness(result)).toBeLessThanOrEqual(255);
        });
    });

    describe('generateVariations', () => {
        test('should generate color variations', () => {
            const variations = colorUtils.generateVariations('#ff0000', 5);
            expect(variations).toHaveLength(5);
            expect(variations.every(color => colorUtils.isValidColor(color))).toBe(true);
        });

        test('should generate different lightness values', () => {
            const variations = colorUtils.generateVariations('#ff0000', 3);
            const brightnesses = variations.map(color => colorUtils.getBrightness(color));
            expect(brightnesses[0]).not.toBe(brightnesses[1]);
            expect(brightnesses[1]).not.toBe(brightnesses[2]);
        });
    });
});
