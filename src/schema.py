from pydantic import BaseModel, Field, RootModel
from typing import Dict, Any, Optional, Union

class TimeseriesData(RootModel[Dict[Union[str, int], Optional[float]]]):
    """Timeseries data structure: timestamp -> value mapping (supports both string and integer timestamps)"""
    root: Dict[Union[str, int], Optional[float]]

class ComputeRequest(BaseModel):
    """Request schema for compute operations"""
    data: Dict[str, TimeseriesData] = Field(..., description="Input sensor and constant data")
    parameters: Dict[str, Any] = Field(default_factory=dict, description="Compute parameters (e.g., window_size for rolling_mean)")
    tick: int = Field(..., description="Current execution timestamp")
    uwid: str = Field(..., description="Unique work identifier")

class ComputeResponse(BaseModel):
    """Response schema for compute operations"""
    data: Dict[str, TimeseriesData] = Field(..., description="Computed output data")
    uwid: str = Field(..., description="Unique work identifier")

class ErrorResponse(BaseModel):
    """Error response schema"""
    issues: list = Field(..., description="List of validation issues")
