# API

This document provides specification of the request and response schemas for a Foundation compatible compute.

## Request Schema

**Example:**

```json
{
  "data": {
    "temperature": {
      "1704110400000": 22.5,
      "1704110460000": 23.1,
      "1704110520000": 21.8
    },
    "humidity": {
      "1704110400000": 65.0,
      "1704110460000": 67.2,
      "1704110520000": 63.8
    }
  },
  "parameters": {
    "window_size": 3
  },
  "tick": 1704110400,
  "uwid": "a2c39e3c-30dd-4e53-ad7d-2ec0c0b35729"
}
```

### data

**Type:** `Dict[str, TimeseriesData]`

**Description:** The data holds the timeseries data for named sensor inputs. The keys are the sensor names and the values are the timeseries data. Timeseries data is a dictionary with timestamps as keys and values as recorded values.

### parameters

**Type:** `Dict[str, Any]`

**Description:** The parameters are the parameters for the compute. Typically the parameters are used to tune the compute internals. In this example, the parameters are used to set the window size for the rolling mean compute.

### tick

**Type:** `int`

**Description:** The tick is the timestamp of the current execution, which basically is the time the compute is executed.

### uwid

**Type:** `str`

**Description:** The uwid is the unique work identifier. It is used to identify the work item and to track the work item through the compute lifecycle.

## Response Schema

**Example:**

```json
{
  "data": {
    "temperature": {
      "1704110400000": 22.5,
      "1704110460000": 22.8,
      "1704110520000": 22.466666666666665
    },
    "humidity": {
      "1704110400000": 65.0,
      "1704110460000": 66.1,
      "1704110520000": 65.33333333333333
    }
  },
  "uwid": "a2c39e3c-30dd-4e53-ad7d-2ec0c0b35729"
}
```

### data

**Type:** `Dict[str, TimeseriesData]`

**Description:** The data holds the timeseries data for named sensor outputs. The keys are the sensor names and the values are the timeseries data. Timeseries data is a dictionary with timestamps as keys and values as recorded values.

### uwid

**Type:** `str`
