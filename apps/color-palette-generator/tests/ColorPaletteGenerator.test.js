/**
 * Tests for ColorPaletteGenerator class
 */

const ColorPaletteGenerator = require('../src/ColorPaletteGenerator');

describe('ColorPaletteGenerator', () => {
    let generator;

    beforeEach(() => {
        generator = new ColorPaletteGenerator();
    });

    describe('generateRandomPalette', () => {
        test('should generate random colors by default', () => {
            const palette = generator.generateRandomPalette('random', 5);
            expect(palette).toHaveLength(5);
            expect(palette.every(color => /^#[0-9a-f]{6}$/.test(color))).toBe(true);
        });

        test('should generate complementary palette', () => {
            const palette = generator.generateComplementaryPalette(4);
            expect(palette).toHaveLength(4);
            expect(palette.every(color => /^#[0-9a-f]{6}$/.test(color))).toBe(true);
        });

        test('should generate triadic palette', () => {
            const palette = generator.generateTriadicPalette(6);
            expect(palette).toHaveLength(6);
            expect(palette.every(color => /^#[0-9a-f]{6}$/.test(color))).toBe(true);
        });

        test('should generate analogous palette', () => {
            const palette = generator.generateAnalogousPalette(5);
            expect(palette).toHaveLength(5);
            expect(palette.every(color => /^#[0-9a-f]{6}$/.test(color))).toBe(true);
        });

        test('should generate monochromatic palette', () => {
            const palette = generator.generateMonochromaticPalette(5);
            expect(palette).toHaveLength(5);
            expect(palette.every(color => /^#[0-9a-f]{6}$/.test(color))).toBe(true);
        });
    });

    describe('generateFromBaseColor', () => {
        test('should generate complementary from base color', () => {
            const palette = generator.generateFromBaseColor('#ff0000', 'complementary', 4);
            expect(palette).toHaveLength(4);
            expect(palette.every(color => /^#[0-9a-f]{6}$/.test(color))).toBe(true);
        });

        test('should generate triadic from base color', () => {
            const palette = generator.generateFromBaseColor('#00ff00', 'triadic', 6);
            expect(palette).toHaveLength(6);
            expect(palette.every(color => /^#[0-9a-f]{6}$/.test(color))).toBe(true);
        });

        test('should generate analogous from base color', () => {
            const palette = generator.generateFromBaseColor('#0000ff', 'analogous', 5);
            expect(palette).toHaveLength(5);
            expect(palette.every(color => /^#[0-9a-f]{6}$/.test(color))).toBe(true);
        });

        test('should generate monochromatic from base color', () => {
            const palette = generator.generateFromBaseColor('#ff00ff', 'monochromatic', 5);
            expect(palette).toHaveLength(5);
            expect(palette.every(color => /^#[0-9a-f]{6}$/.test(color))).toBe(true);
        });

        test('should handle different color formats', () => {
            const hexPalette = generator.generateFromBaseColor('#ff0000', 'complementary', 3);
            const rgbPalette = generator.generateFromBaseColor('rgb(255, 0, 0)', 'complementary', 3);
            const hslPalette = generator.generateFromBaseColor('hsl(0, 100%, 50%)', 'complementary', 3);
            
            expect(hexPalette).toHaveLength(3);
            expect(rgbPalette).toHaveLength(3);
            expect(hslPalette).toHaveLength(3);
        });

        test('should throw error for invalid base color', () => {
            expect(() => {
                generator.generateFromBaseColor('invalid', 'complementary', 3);
            }).toThrow();
        });
    });

    describe('specialized palettes', () => {
        test('should generate warm palette', () => {
            const palette = generator.generateWarmPalette(5);
            expect(palette).toHaveLength(5);
            expect(palette.every(color => /^#[0-9a-f]{6}$/.test(color))).toBe(true);
        });

        test('should generate cool palette', () => {
            const palette = generator.generateCoolPalette(5);
            expect(palette).toHaveLength(5);
            expect(palette.every(color => /^#[0-9a-f]{6}$/.test(color))).toBe(true);
        });

        test('should generate pastel palette', () => {
            const palette = generator.generatePastelPalette(5);
            expect(palette).toHaveLength(5);
            expect(palette.every(color => /^#[0-9a-f]{6}$/.test(color))).toBe(true);
        });

        test('should generate vibrant palette', () => {
            const palette = generator.generateVibrantPalette(5);
            expect(palette).toHaveLength(5);
            expect(palette.every(color => /^#[0-9a-f]{6}$/.test(color))).toBe(true);
        });
    });

    describe('seed functionality', () => {
        test('should generate same palette with same seed', () => {
            generator.setSeed(12345);
            const palette1 = generator.generateRandomPalette('random', 5);
            
            generator.setSeed(12345);
            const palette2 = generator.generateRandomPalette('random', 5);
            
            expect(palette1).toEqual(palette2);
        });

        test('should generate different palettes with different seeds', () => {
            generator.setSeed(12345);
            const palette1 = generator.generateRandomPalette('random', 5);
            
            generator.setSeed(54321);
            const palette2 = generator.generateRandomPalette('random', 5);
            
            expect(palette1).not.toEqual(palette2);
        });
    });

    describe('getPaletteInfo', () => {
        test('should return comprehensive palette information', () => {
            const palette = ['#ff0000', '#00ff00', '#0000ff'];
            const info = generator.getPaletteInfo(palette);
            
            expect(info).toHaveProperty('count', 3);
            expect(info).toHaveProperty('colors', palette);
            expect(info).toHaveProperty('formats');
            expect(info).toHaveProperty('brightness');
            expect(info).toHaveProperty('isLight');
            
            expect(info.formats).toHaveProperty('hex');
            expect(info.formats).toHaveProperty('rgb');
            expect(info.formats).toHaveProperty('hsl');
            
            expect(info.brightness).toHaveLength(3);
            expect(info.isLight).toHaveLength(3);
        });
    });

    describe('edge cases', () => {
        test('should handle zero count', () => {
            const palette = generator.generateRandomPalette('random', 0);
            expect(palette).toHaveLength(0);
        });

        test('should handle single color', () => {
            const palette = generator.generateRandomPalette('random', 1);
            expect(palette).toHaveLength(1);
            expect(/^#[0-9a-f]{6}$/.test(palette[0])).toBe(true);
        });

        test('should handle large count', () => {
            const palette = generator.generateRandomPalette('random', 100);
            expect(palette).toHaveLength(100);
            expect(palette.every(color => /^#[0-9a-f]{6}$/.test(color))).toBe(true);
        });
    });

    describe('color scheme validation', () => {
        test('should handle unknown scheme gracefully', () => {
            const palette = generator.generateRandomPalette('unknown', 5);
            expect(palette).toHaveLength(5);
            expect(palette.every(color => /^#[0-9a-f]{6}$/.test(color))).toBe(true);
        });

        test('should handle case insensitive schemes', () => {
            const palette1 = generator.generateRandomPalette('COMPLEMENTARY', 5);
            const palette2 = generator.generateRandomPalette('complementary', 5);
            expect(palette1).toHaveLength(5);
            expect(palette2).toHaveLength(5);
        });
    });
});
