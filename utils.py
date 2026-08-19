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
    Check whether a filename has an allowed extension.
    """

    if not filename:
        return False

    if "." not in filename:
        return False

    extension = get_file_extension(filename)

    return extension in Config.ALLOWED_EXTENSIONS


# ============================================================
# Filename Generation
# ============================================================

def generate_filename(filename: str) -> str:
    """
    Generate a secure and unique filename.
    """

    if not filename:
        return ""

    secure_name = secure_filename(filename)

    if not secure_name:
        return ""

    extension = get_file_extension(
        secure_name
    )

    if not extension:
        return ""

    if extension not in Config.ALLOWED_EXTENSIONS:
        return ""

    return (
        f"{uuid.uuid4().hex}"
        f".{extension}"
    )


# ============================================================
# File Saving
# ============================================================

def save_uploaded_file(
    file: FileStorage,
    upload_folder: str
) -> Tuple[str, str]:
    """
    Safely save an uploaded file.

    Returns:
        Tuple[str, str]:
            Full file path and generated filename.
    """

    if file is None:
        raise ValueError(
            "No file was provided."
        )

    if not file.filename:
        raise ValueError(
            "Filename is empty."
        )

    if not allowed_file(file.filename):
        raise ValueError(
            "File type is not allowed."
        )

    filename = generate_filename(
        file.filename
    )

    if not filename:
        raise ValueError(
            "Invalid filename."
        )

    create_directory(
        upload_folder
    )

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

def create_directory(
    path: Optional[str]
) -> None:
    """
    Create a directory if it does not exist.
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

def delete_file(
    filepath: Optional[str]
) -> bool:
    """
    Delete a file if it exists.
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

def get_file_extension(
    filename: str
) -> str:
    """
    Return the file extension without the dot.

    Example:
        image.jpg -> jpg
    """

    if not filename:
        return ""

    if "." not in filename:
        return ""

    return filename.rsplit(
        ".",
        1
    )[1].lower()


# ============================================================
# Filename Without Extension
# ============================================================

def get_filename(
    filename: str
) -> str:
    """
    Return the filename without its extension.

    Example:
        /uploads/image.jpg -> image
    """

    if not filename:
        return ""

    return os.path.splitext(
        os.path.basename(filename)
    )[0]