/**
 * Color Utilities
 * 
 * Provides utility functions for color conversion and manipulation.
 */

class ColorUtils {
    /**
     * Convert hex color to RGB
     */
    hexToRgb(hex) {
        const result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
        if (!result) {
            throw new Error(`Invalid hex color: ${hex}`);
        }
        
        const r = parseInt(result[1], 16);
        const g = parseInt(result[2], 16);
        const b = parseInt(result[3], 16);
        
        return `rgb(${r}, ${g}, ${b})`;
    }

    /**
     * Convert RGB to hex
     */
    rgbToHex(rgb) {
        const result = rgb.match(/\d+/g);
        if (!result || result.length !== 3) {
            throw new Error(`Invalid RGB color: ${rgb}`);
        }
        
        const r = parseInt(result[0]);
        const g = parseInt(result[1]);
        const b = parseInt(result[2]);
        
        return `#${((1 << 24) + (r << 16) + (g << 8) + b).toString(16).slice(1)}`;
    }

    /**
     * Convert hex to HSL
     */
    hexToHsl(hex) {
        const rgb = this.hexToRgb(hex);
        const result = rgb.match(/\d+/g);
        const r = parseInt(result[0]) / 255;
        const g = parseInt(result[1]) / 255;
        const b = parseInt(result[2]) / 255;

        const max = Math.max(r, g, b);
        const min = Math.min(r, g, b);
        let h, s, l = (max + min) / 2;

        if (max === min) {
            h = s = 0; // achromatic
        } else {
            const d = max - min;
            s = l > 0.5 ? d / (2 - max - min) : d / (max + min);
            
            switch (max) {
                case r: h = (g - b) / d + (g < b ? 6 : 0); break;
                case g: h = (b - r) / d + 2; break;
                case b: h = (r - g) / d + 4; break;
            }
            h /= 6;
        }

        return `hsl(${Math.round(h * 360)}, ${Math.round(s * 100)}%, ${Math.round(l * 100)}%)`;
    }

    /**
     * Convert HSL to hex
     */
    hslToHex(hsl) {
        const result = hsl.match(/\d+/g);
        if (!result || result.length !== 3) {
            throw new Error(`Invalid HSL color: ${hsl}`);
        }
        
        const h = parseInt(result[0]) / 360;
        const s = parseInt(result[1]) / 100;
        const l = parseInt(result[2]) / 100;

        const hue2rgb = (p, q, t) => {
            if (t < 0) t += 1;
            if (t > 1) t -= 1;
            if (t < 1/6) return p + (q - p) * 6 * t;
            if (t < 1/2) return q;
            if (t < 2/3) return p + (q - p) * (2/3 - t) * 6;
            return p;
        };

        let r, g, b;

        if (s === 0) {
            r = g = b = l; // achromatic
        } else {
            const q = l < 0.5 ? l * (1 + s) : l + s - l * s;
            const p = 2 * l - q;
            r = hue2rgb(p, q, h + 1/3);
            g = hue2rgb(p, q, h);
            b = hue2rgb(p, q, h - 1/3);
        }

        const toHex = (c) => {
            const hex = Math.round(c * 255).toString(16);
            return hex.length === 1 ? '0' + hex : hex;
        };

        return `#${toHex(r)}${toHex(g)}${toHex(b)}`;
    }

    /**
     * Validate if a color string is valid
     */
    isValidColor(color) {
        if (!color || typeof color !== 'string') {
            return false;
        }

        // Check hex format
        if (/^#?[0-9A-Fa-f]{6}$/.test(color)) {
            return true;
        }

        // Check RGB format
        if (/^rgb\(\s*\d+\s*,\s*\d+\s*,\s*\d+\s*\)$/.test(color)) {
            return true;
        }

        // Check HSL format
        if (/^hsl\(\s*\d+\s*,\s*\d+%\s*,\s*\d+%\s*\)$/.test(color)) {
            return true;
        }

        return false;
    }

    /**
     * Normalize color to hex format
     */
    normalizeToHex(color) {
        if (!this.isValidColor(color)) {
            throw new Error(`Invalid color format: ${color}`);
        }

        if (color.startsWith('#')) {
            return color;
        } else if (color.startsWith('rgb')) {
            return this.rgbToHex(color);
        } else if (color.startsWith('hsl')) {
            return this.hslToHex(color);
        }

        throw new Error(`Unsupported color format: ${color}`);
    }

    /**
     * Generate random hex color
     */
    generateRandomHex() {
        return '#' + Math.floor(Math.random() * 16777215).toString(16).padStart(6, '0');
    }

    /**
     * Get color brightness (0-255)
     */
    getBrightness(hex) {
        const rgb = this.hexToRgb(hex);
        const result = rgb.match(/\d+/g);
        const r = parseInt(result[0]);
        const g = parseInt(result[1]);
        const b = parseInt(result[2]);
        
        return Math.round((r * 299 + g * 587 + b * 114) / 1000);
    }

    /**
     * Check if color is light or dark
     */
    isLight(hex) {
        return this.getBrightness(hex) > 128;
    }

    /**
     * Get contrasting color (black or white)
     */
    getContrastColor(hex) {
        return this.isLight(hex) ? '#000000' : '#ffffff';
    }

    /**
     * Adjust color brightness
     */
    adjustBrightness(hex, percent) {
        const rgb = this.hexToRgb(hex);
        const result = rgb.match(/\d+/g);
        let r = parseInt(result[0]);
        let g = parseInt(result[1]);
        let b = parseInt(result[2]);

        r = Math.max(0, Math.min(255, Math.round(r * (1 + percent / 100))));
        g = Math.max(0, Math.min(255, Math.round(g * (1 + percent / 100))));
        b = Math.max(0, Math.min(255, Math.round(b * (1 + percent / 100))));

        return this.rgbToHex(`rgb(${r}, ${g}, ${b})`);
    }

    /**
     * Generate color variations
     */
    generateVariations(baseColor, count = 5) {
        const hex = this.normalizeToHex(baseColor);
        const hsl = this.hexToHsl(hex);
        const result = hsl.match(/\d+/g);
        const h = parseInt(result[0]);
        const s = parseInt(result[1]);
        const l = parseInt(result[2]);

        const variations = [];
        const step = 100 / (count - 1);

        for (let i = 0; i < count; i++) {
            const newL = Math.max(10, Math.min(90, l + (i * step - 50)));
            const variation = `hsl(${h}, ${s}%, ${newL}%)`;
            variations.push(this.hslToHex(variation));
        }

        return variations;
    }
}

module.exports = ColorUtils;
