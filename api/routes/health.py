# ============================================
# Health Check Route
# GET /api/health
# ============================================

from flask import Blueprint, jsonify

health_bp = Blueprint("health", __name__)


@health_bp.route("/health", methods=["GET"])
def health_check():
    """Simple health check endpoint"""
    return jsonify({
        "status" : "ok",
        "message": "Student Performance Advisor API is running",
        "version": "1.0.0"
    }), 200