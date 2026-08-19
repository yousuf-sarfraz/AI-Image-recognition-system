# ============================================================
# Flask Application
# Image & Text Recognition AI
# ============================================================

import logging
import os

from flask import (
    Flask,
    jsonify,
    send_from_directory
)

from config import Config
from routes.main import main


# ============================================================
# Logging
# ============================================================

logging.basicConfig(
    level=logging.INFO,
    format=(
        "%(asctime)s - "
        "%(name)s - "
        "%(levelname)s - "
        "%(message)s"
    )
)

logger = logging.getLogger(__name__)


# ============================================================
# Application Factory
# ============================================================

def create_app():
    """
    Create and configure the Flask application.
    """

    app = Flask(__name__)

    # --------------------------------------------------------
    # Load configuration
    # --------------------------------------------------------

    app.config.from_object(Config)

    # --------------------------------------------------------
    # Create required directories
    # --------------------------------------------------------

    Config.create_directories()

    # --------------------------------------------------------
    # Register routes
    # --------------------------------------------------------

    app.register_blueprint(main)

    # --------------------------------------------------------
    # Uploaded files
    # --------------------------------------------------------

    @app.route("/uploads/<path:filename>")
    def uploaded_file(filename):
        """
        Serve uploaded images.
        """

        return send_from_directory(
            app.config["UPLOAD_FOLDER"],
            filename
        )

    # --------------------------------------------------------
    # Application errors
    # --------------------------------------------------------

    @app.errorhandler(413)
    def file_too_large(error):
        """
        Handle files larger than MAX_CONTENT_LENGTH.
        """

        return jsonify(
            {
                "success": False,
                "error": "File is too large. Maximum size is 16 MB."
            }
        ), 413

    @app.errorhandler(404)
    def page_not_found(error):
        """
        Handle unknown routes.
        """

        return jsonify(
            {
                "success": False,
                "error": "Page not found."
            }
        ), 404

    @app.errorhandler(500)
    def internal_server_error(error):
        """
        Handle unexpected server errors.
        """

        logger.exception(
            "Internal server error"
        )

        return jsonify(
            {
                "success": False,
                "error": "Internal server error."
            }
        ), 500

    logger.info(
        "Flask application created successfully."
    )

    return app


# ============================================================
# Run Application
# ============================================================

if __name__ == "__main__":

    app = create_app()

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )