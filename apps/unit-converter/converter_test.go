package converter

import "testing"

func TestConvertLength(t *testing.T) {
	tests := []struct {
		name     string
		kind     string
		value    float64
		expected float64
	}{
		{"meters to feet", "m2ft", 1, 3.28084},
		{"feet to meters", "ft2m", 3.28084, 1},
	}

	for _, tc := range tests {
		t.Run(tc.name, func(t *testing.T) {
			got, err := Convert(tc.kind, tc.value)
			if err != nil {
				t.Fatalf("unexpected error: %v", err)
			}
			if diff := got - tc.expected; diff > 1e-5 || diff < -1e-5 {
				t.Fatalf("expected %.5f, got %.5f", tc.expected, got)
			}
		})
	}
}

func TestConvertTemperature(t *testing.T) {
	tests := []struct {
		name     string
		kind     string
		value    float64
		expected float64
	}{
		{"celsius to fahrenheit", "c2f", 0, 32},
		{"fahrenheit to celsius", "f2c", 212, 100},
	}

	for _, tc := range tests {
		t.Run(tc.name, func(t *testing.T) {
			got, err := Convert(tc.kind, tc.value)
			if err != nil {
				t.Fatalf("unexpected error: %v", err)
			}
			if diff := got - tc.expected; diff > 1e-5 || diff < -1e-5 {
				t.Fatalf("expected %.2f, got %.2f", tc.expected, got)
			}
		})
	}
}

func TestConvertInvalid(t *testing.T) {
	if _, err := Convert("invalid", 42); err == nil {
		t.Fatal("expected error for invalid conversion")
	}
}
