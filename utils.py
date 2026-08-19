# ============================================================
# Utility Functions
# Image & Text Recognition AI
# ============================================================

import os
import uuid
from typing import Optional, Tuple

from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename

from config import Config


# ============================================================
# File Validation
# ============================================================

def allowed_file(filename: str) -> bool:
    """
    Check whether the uploaded file has an allowed extension.

    Parameters
    ----------
    filename : str
        Name of the uploaded file.

    Returns
    -------
    bool
        True if the file extension is allowed, otherwise False.
    """

    if not filename or "." not in filename:
        return False

    extension = filename.rsplit(".", 1)[1].lower()

    return extension in Config.ALLOWED_EXTENSIONS


# ============================================================
# Filename Generation
# ============================================================

def generate_filename(filename: str) -> str:
    """
    Generate a secure and unique filename.

    The original filename is sanitized and only its extension
    is preserved. A UUID is used to prevent filename conflicts.

    Parameters
    ----------
    filename : str
        Original uploaded filename.

    Returns
    -------
    str
        Unique secure filename, or empty string if invalid.
    """

    if not filename:
        return ""

    secure_name = secure_filename(filename)

    if not secure_name or "." not in secure_name:
        return ""

    extension = secure_name.rsplit(".", 1)[1].lower()

    if extension not in Config.ALLOWED_EXTENSIONS:
        return ""

    return f"{uuid.uuid4().hex}.{extension}"


# ============================================================
# File Saving
# ============================================================

def save_uploaded_file(
    file: FileStorage,
    upload_folder: str
) -> Tuple[str, str]:
    """
    Safely save an uploaded file.

    Parameters
    ----------
    file : FileStorage
        Uploaded Flask/Werkzeug file object.

    upload_folder : str
        Directory where the file should be saved.

    Returns
    -------
    Tuple[str, str]
        Full file path and generated filename.

    Raises
    ------
    ValueError
        If the uploaded file or filename is invalid.
    """

    if file is None:
        raise ValueError("No file was provided.")

    if not file.filename:
        raise ValueError("Filename is empty.")

    if not allowed_file(file.filename):
        raise ValueError("File type is not allowed.")

    filename = generate_filename(file.filename)

    if not filename:
        raise ValueError("Invalid filename.")

    create_directory(upload_folder)

    filepath = os.path.join(
        upload_folder,
        filename
    )

    try:
        file.save(filepath)

    except OSError as error:
        raise OSError(
            f"Failed to save uploaded file: {error}"
        ) from error

    return filepath, filename


# ============================================================
# Directory
# ============================================================

def create_directory(path: Optional[str]) -> None:
    """
    Create a directory if it does not already exist.

    Parameters
    ----------
    path : str | None
        Directory path.
    """

    if not path:
        return

    try:
        os.makedirs(
            path,
            exist_ok=True
        )

    except OSError as error:
        raise OSError(
            f"Failed to create directory: {path}"
        ) from error


# ============================================================
# File Deletion
# ============================================================

def delete_file(filepath: Optional[str]) -> bool:
    """
    Delete a file if it exists.

    Parameters
    ----------
    filepath : str | None
        Path of the file to delete.

    Returns
    -------
    bool
        True if the file was deleted,
        False if it did not exist or deletion failed.
    """

    if not filepath:
        return False

    if not os.path.isfile(filepath):
        return False

    try:
        os.remove(filepath)
        return True

    except OSError:
        return False


# ============================================================
# File Extension
# ============================================================

def get_file_extension(filename: str) -> str:
    """
    Return the file extension without the dot.

    Example
    -------
    "image.jpg" -> "jpg"
    """

    if not filename or "." not in filename:
        return ""

    return filename.rsplit(
        ".",
        1
    )[1].lower()


# ============================================================
# Filename Without Extension
# ============================================================

def get_filename(filename: str) -> str:
    """
    Return the filename without its extension.

    Example
    -------
    "/uploads/image.jpg" -> "image"
    """

    if not filename:
        return ""

    return os.path.splitext(
        os.path.basename(filename)
    )[0]