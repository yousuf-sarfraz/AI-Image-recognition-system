from flask import Flask, send_from_directory

from config import Config
from routes.main import main


def create_app():
    """
    Application Factory.

    Creates and configures the Flask application,
    registers routes, and prepares required directories.
    """

    # Create Flask application
    app = Flask(__name__)

    # Load application configuration
    app.config.from_object(Config)

    # Create required project directories
    Config.create_directories()

    # Register main application routes
    app.register_blueprint(main)

    # Serve uploaded images
    @app.route("/uploads/<filename>")
    def uploaded_file(filename):
        return send_from_directory(
            app.config["UPLOAD_FOLDER"],
            filename
        )

    return app


# Run application directly
if __name__ == "__main__":
    app = create_app()

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )