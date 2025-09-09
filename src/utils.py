"""
Utility functions for data conversion and processing.
"""

from typing import Dict, Optional, Tuple
import pandas as pd
from schema import TimeseriesData


def to_dataframe(sensor_data: TimeseriesData) -> Tuple[Optional[pd.DataFrame], Optional[list]]:
    """Convert TimeseriesData to pandas DataFrame, returning original timestamps for format preservation."""
    if not sensor_data.root:
        return None, None
        
    timestamps = []
    values = []
    original_timestamps = []
    
    for ts, val in sensor_data.root.items():
        if val is not None:
            original_timestamps.append(ts)
            if isinstance(ts, str) and ts.isdigit():
                ts_int = int(ts)
                timestamps.append(pd.to_datetime(ts_int, unit='ms'))
            elif isinstance(ts, int):
                timestamps.append(pd.to_datetime(ts, unit='ms'))
            else:
                timestamps.append(pd.to_datetime(ts))
            values.append(val)
    
    if timestamps and values:
        df = pd.DataFrame({'timestamp': timestamps, 'value': values}).set_index('timestamp')
        return df, original_timestamps
    
    return None, None


def to_response(series: pd.Series, original_timestamps: Optional[list] = None) -> TimeseriesData:
    """Convert pandas Series to TimeseriesData format, preserving original timestamp format."""
    result = {}
    
    for i, (timestamp, value) in enumerate(series.items()):
        if original_timestamps and i < len(original_timestamps):
            original_ts = original_timestamps[i]
            if isinstance(original_ts, str) and original_ts.isdigit():
                result[original_ts] = float(value) if pd.notna(value) else None
            elif isinstance(original_ts, int):
                result[original_ts] = float(value) if pd.notna(value) else None
            else:
                result[timestamp.isoformat()] = float(value) if pd.notna(value) else None
        else:
            timestamp_int = int(timestamp.timestamp() * 1000)
            result[timestamp_int] = float(value) if pd.notna(value) else None
    
    return TimeseriesData(result)
