#!/usr/bin/env python3
"""
Foundation HTTP Compute Example

This is a Python Flask-based HTTP compute service that demonstrates how to
implement a compute compatible with the Foundation platform.

The service handles HTTP requests from Foundation compute workers and performs
simple computation and returns the result.
"""

import json
import logging
import uuid
from datetime import datetime
from typing import Dict, Any, Optional, Union, Tuple
from flask import Flask, request, jsonify
from pydantic import BaseModel, Field, ValidationError
import numpy as np
import pandas as pd
from scipy import signal
from schema import TimeseriesData, ComputeRequest, ComputeResponse, ErrorResponse
from compute import Compute

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

compute_service = Compute()

@app.route('/execute/<compute_name>', methods=['POST'])
def execute_compute(compute_name: str):
    """Main compute endpoint with compute name parameter"""
    try:
        valid_computes = ['rolling_mean']
        if compute_name not in valid_computes:
            error_response = ErrorResponse(
                issues=[{
                    'code': 'invalid_compute_name',
                    'message': f"Invalid compute name '{compute_name}'. Valid options: {', '.join(valid_computes)}",
                    'path': ['compute_name']
                }]
            )
            return jsonify(error_response.dict()), 400

        request_data = ComputeRequest(**request.json)
        result = compute_service.execute(request_data, compute_name)
        return jsonify(result.dict()), 200

    except ValidationError as e:
        error_response = ErrorResponse(
            issues=[{
                'code': error['type'],
                'message': error['msg'],
                'path': list(error['loc'])
            } for error in e.errors()]
        )
        return jsonify(error_response.dict()), 400

    except Exception as e:
        logger.error(f"Computation failed: {str(e)}")
        error_response = ErrorResponse(
            issues=[{
                'code': 'internal_error',
                'message': str(e),
                'path': []
            }]
        )
        return jsonify(error_response.dict()), 500

@app.route('/healthz', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return 'OK', 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8060, debug=True)
