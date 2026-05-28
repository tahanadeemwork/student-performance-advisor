# ============================================
# Sample Profiles Route
# GET /api/samples
# ============================================

import sys
import os
sys.path.append(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)

from flask import Blueprint, jsonify
from tests.test_scenarios import get_all_scenarios

samples_bp = Blueprint("samples", __name__)


@samples_bp.route("/samples", methods=["GET"])
def get_samples():
    """Returns all sample student profiles"""
    try:
        scenarios = get_all_scenarios()
        samples   = []

        for name, data in scenarios:
            samples.append({
                "name"   : name,
                "profile": data
            })

        return jsonify({
            "success": True,
            "count"  : len(samples),
            "samples": samples
        }), 200

    except Exception as e:
        return jsonify({
            "success": False,
            "error"  : str(e)
        }), 500