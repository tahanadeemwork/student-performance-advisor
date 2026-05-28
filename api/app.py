# ============================================
# Flask Application
# Student Performance Prediction Advisor API
# ============================================

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask      import Flask
from flask_cors import CORS

from api.config         import config
from api.routes.health  import health_bp
from api.routes.analyze import analyze_bp
from api.routes.samples import samples_bp


def create_app(config_name="development"):
    """Create and configure Flask application"""

    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # Enable CORS for React frontend
    CORS(app, resources={
        r"/api/*": {
            "origins": "*",
            "methods": ["GET", "POST", "OPTIONS"],
            "allow_headers": ["Content-Type"]
        }
    })

    # Register blueprints
    app.register_blueprint(health_bp, url_prefix="/api")
    app.register_blueprint(analyze_bp, url_prefix="/api")
    app.register_blueprint(samples_bp, url_prefix="/api")

    return app


# Run the app
if __name__ == "__main__":
    app = create_app("development")
    print("\n🚀 Flask API Starting...")
    print("   URL    : http://localhost:5000")
    print("   Health : http://localhost:5000/api/health")
    print("   Analyze: http://localhost:5000/api/analyze")
    print("   Samples: http://localhost:5000/api/samples\n")
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )