# foundation-compute-example

Example of a Python compute compatible with the Foundation platform.

## Documentation

- **[API Schema Documentation](API_SCHEMA.md)** - Specification of request and response schemas

## Installation

This project uses Poetry for dependency management. Install Poetry if you haven't already:

```bash
pipx install poetry
```

Then install dependencies:

```bash
poetry install
```

## Running the service

Start the service:

```bash
poetry run python src/main.py
```

The service will be available at `http://localhost:8060`

## Example Usage

### 1. Health Check

```bash
curl http://localhost:8060/healthz
# Returns: OK
```

### 2. Execute Rolling Mean Computation

The rolling mean computation supports a configurable window size parameter. If not specified, it defaults to 3.

#### Default Window Size (3)

```bash
curl -X POST http://localhost:8060/execute/rolling_mean \
  -H "Content-Type: application/json" \
  -d '{
    "data": {
      "sensor1": {
        "1704110400000": 10.0,
        "1704110460000": 12.0,
        "1704110520000": 8.0,
        "1704110580000": 15.0,
        "1704110640000": 11.0
      }
    },
    "parameters": {},
    "tick": 1704110400,
    "uwid": "a2c39e3c-30dd-4e53-ad7d-2ec0c0b35729"
  }'
```

**Response:**

```json
{
  "data": {
    "sensor1": {
      "1704110400000": 10.0,
      "1704110460000": 11.0,
      "1704110520000": 10.0,
      "1704110580000": 11.666666666666666,
      "1704110640000": 11.333333333333334
    }
  },
  "uwid": "a2c39e3c-30dd-4e53-ad7d-2ec0c0b35729"
}
```

#### Custom Window Size (2)

```bash
curl -X POST http://localhost:8060/execute/rolling_mean \
  -H "Content-Type: application/json" \
  -d '{
    "data": {
      "sensor1": {
        "1704110400000": 10.0,
        "1704110460000": 12.0,
        "1704110520000": 8.0,
        "1704110580000": 15.0,
        "1704110640000": 11.0
      }
    },
    "parameters": {"window_size": 2},
    "tick": 1704110400,
    "uwid": "89c4996e-2822-40f3-b9fd-c55685c606f9"
  }'
```

**Response:**

```json
{
  "data": {
    "sensor1": {
      "1704110400000": 10.0,
      "1704110460000": 11.0,
      "1704110520000": 10.0,
      "1704110580000": 11.5,
      "1704110640000": 13.0
    }
  },
  "uwid": "89c4996e-2822-40f3-b9fd-c55685c606f9"
}
```

#### Custom Window Size (4)

```bash
curl -X POST http://localhost:8060/execute/rolling_mean \
  -H "Content-Type: application/json" \
  -d '{
    "data": {
      "sensor1": {
        "1704110400000": 10.0,
        "1704110460000": 12.0,
        "1704110520000": 8.0,
        "1704110580000": 15.0,
        "1704110640000": 11.0
      }
    },
    "parameters": {"window_size": 4},
    "tick": 1704110400,
    "uwid": "0e52793a-3201-4d02-9f77-776a64ae522b"
  }'
```

**Response:**

```json
{
  "data": {
    "sensor1": {
      "1704110400000": 10.0,
      "1704110460000": 11.0,
      "1704110520000": 10.0,
      "1704110580000": 11.25,
      "1704110640000": 11.5
    }
  },
  "uwid": "0e52793a-3201-4d02-9f77-776a64ae522b"
}
```

#### 3. Multiple Input Sensors

The rolling mean computation can process multiple sensor inputs simultaneously:

```bash
curl -X POST http://localhost:8060/execute/rolling_mean \
  -H "Content-Type: application/json" \
  -d '{
    "data": {
      "temperature": {
        "1704110400000": 22.5,
        "1704110460000": 23.1,
        "1704110520000": 21.8,
        "1704110580000": 24.2,
        "1704110640000": 23.7
      },
      "humidity": {
        "1704110400000": 65.0,
        "1704110460000": 67.2,
        "1704110520000": 63.8,
        "1704110580000": 69.1,
        "1704110640000": 66.5
      }
    },
    "parameters": {"window_size": 3},
    "tick": 1704110400,
    "uwid": "2b38a400-7a63-490a-a414-e4efbe478fb2"
  }'
```

**Response:**

```json
{
  "data": {
    "temperature": {
      "1704110400000": 22.5,
      "1704110460000": 22.8,
      "1704110520000": 22.466666666666665,
      "1704110580000": 23.033333333333335,
      "1704110640000": 23.233333333333334
    },
    "humidity": {
      "1704110400000": 65.0,
      "1704110460000": 66.1,
      "1704110520000": 65.33333333333333,
      "1704110580000": 66.7,
      "1704110640000": 66.46666666666665
    }
  },
  "uwid": "2b38a400-7a63-490a-a414-e4efbe478fb2"
}
```

#### 4. Test Invalid Compute Name (Error Handling)

```bash
curl -X POST http://localhost:8060/execute/invalid_compute \
  -H "Content-Type: application/json" \
  -d '{
    "data": {
      "sensor1": {
        "2024-01-01T10:00:00": 10.0
      }
    },
    "parameters": {},
    "tick": 1704110400,
    "uwid": "test-invalid"
  }'
```

**Expected Error Response:**

```json
{
  "issues": [
    {
      "code": "invalid_compute_name",
      "message": "Invalid compute name 'invalid_compute'. Valid options: rolling_mean",
      "path": ["compute_name"]
    }
  ]
}
```
