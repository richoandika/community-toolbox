package converter

import "errors"

const (
	metersToFeetFactor = 3.28084
	feetToMetersFactor = 0.3048
)

// Convert applies the given conversion keyword to the value.
// Supported conversions:
//   - "m2ft": meters to feet
//   - "ft2m": feet to meters
//   - "c2f": Celsius to Fahrenheit
//   - "f2c": Fahrenheit to Celsius
func Convert(kind string, value float64) (float64, error) {
	switch kind {
	case "m2ft":
		return value * metersToFeetFactor, nil
	case "ft2m":
		return value * feetToMetersFactor, nil
	case "c2f":
		return value*9.0/5.0 + 32, nil
	case "f2c":
		return (value - 32) * 5.0 / 9.0, nil
	default:
		return 0, errors.New("unsupported conversion")
	}
}
