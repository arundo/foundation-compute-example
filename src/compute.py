"""
Compute service class containing computation logic.
"""

import logging
import pandas as pd
from typing import Dict, Any, Optional
from schema import ComputeRequest, ComputeResponse, TimeseriesData
from utils import to_response, to_dataframe


class Compute:
    """Class containing computation logic"""

    def __init__(self):
        self.logger = logging.getLogger(f"{__name__}.ComputeService")

    def execute(self, request_data: ComputeRequest, compute_name: str) -> ComputeResponse:
        """Execute the main computation based on the request data and compute name."""
        self.logger.info(f"Executing {compute_name} computation for uwid: {request_data.uwid}")
        
        if compute_name == 'rolling_mean':
            window_size = max(1, request_data.parameters.get('window_size', 3))
            result_data = self._compute_rolling_mean(request_data.data, window_size)
        else:
            raise ValueError(f"Unknown compute name: {compute_name}")
        
        self.logger.info(f"Computation completed for uwid: {request_data.uwid}")
        return ComputeResponse(data=result_data, uwid=request_data.uwid)

    def _compute_rolling_mean(self, input_data: Dict[str, TimeseriesData], window_size: int) -> Dict[str, TimeseriesData]:
        """Calculate rolling mean for all sensors."""
        result_data = {}
        
        for sensor_name, sensor_data in input_data.items():
            if sensor_data.root:
                df, original_timestamps = to_dataframe(sensor_data)
                if df is not None:
                    rolling_series = df['value'].rolling(window=window_size, min_periods=1).mean()
                    result_data[sensor_name] = to_response(rolling_series, original_timestamps)
        
        return result_data
    

