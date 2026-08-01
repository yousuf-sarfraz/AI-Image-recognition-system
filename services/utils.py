import os
import uuid
from werkzeug.utils import secure_filename

from config import Config


def allowed_file(filename):
    """
    Check whether the uploaded file has
    an allowed image extension.
    """

    if "." not in filename:
        return False

    extension = filename.rsplit(".", 1)[1].lower()

    return extension in Config.ALLOWED_EXTENSIONS


def generate_filename(filename):
    """
    Generate a unique filename to prevent
    overwriting existing files.
    """

    extension = filename.rsplit(".", 1)[1].lower()

    unique_name = f"{uuid.uuid4().hex}.{extension}"

    return unique_name


def save_uploaded_file(file, upload_folder):
    """
    Save uploaded image safely and return
    the saved file path.
    """

    filename = secure_filename(file.filename)

    filename = generate_filename(filename)

    filepath = os.path.join(upload_folder, filename)

    file.save(filepath)

    return filepath, filename


def create_directory(path):
    """
    Create directory if it does not exist.
    """

    os.makedirs(path, exist_ok=True)


def delete_file(filepath):
    """
    Delete file if it exists.
    """

    if os.path.exists(filepath):
        os.remove(filepath)


def get_file_extension(filename):
    """
    Return file extension.
    """

    return filename.rsplit(".", 1)[1].lower()


def get_filename(filename):
    """
    Return filename without extension.
    """

    return os.path.splitext(filename)[0]