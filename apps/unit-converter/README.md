# Unit Converter (Go)

This Go package provides simple conversions between common units:

- meters to feet (`m2ft`)
- feet to meters (`ft2m`)
- Celsius to Fahrenheit (`c2f`)
- Fahrenheit to Celsius (`f2c`)

## Usage

```go
result, err := converter.Convert("m2ft", 1)
```

## Running Tests

```bash
go test ./...
```
