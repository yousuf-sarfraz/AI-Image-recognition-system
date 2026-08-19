/* ==========================================
   Image & Text Recognition AI
   Frontend JavaScript
========================================== */

document.addEventListener("DOMContentLoaded", () => {

    /* ==========================================
       Elements
    ========================================== */

    const imageInput = document.getElementById("image");
    const previewImage = document.getElementById("preview-image");
    const uploadBox = document.querySelector(".upload-box");
    const uploadLabel = document.querySelector(".upload-box label");
    const fileName = document.getElementById("file-name");
    const form = document.querySelector("form");
    const loading = document.getElementById("loading");

    /* ==========================================
       Configuration
    ========================================== */

    const MAX_FILE_SIZE = 16 * 1024 * 1024;

    const ALLOWED_TYPES = new Set([
        "image/jpeg",
        "image/png",
        "image/bmp",
        "image/webp"
    ]);


    /* ==========================================
       Utility Functions
    ========================================== */

    function formatFileSize(bytes) {

        if (bytes < 1024) {
            return `${bytes} B`;
        }

        if (bytes < 1024 * 1024) {
            return `${(bytes / 1024).toFixed(1)} KB`;
        }

        return `${(bytes / (1024 * 1024)).toFixed(2)} MB`;
    }


    function removeMessage() {

        const existingMessage =
            document.querySelector(".js-upload-message");

        if (existingMessage) {
            existingMessage.remove();
        }
    }


    function showMessage(message, type = "error") {

        removeMessage();

        const messageElement =
            document.createElement("div");

        messageElement.className =
            `js-upload-message ${type}`;

        messageElement.setAttribute(
            "role",
            "alert"
        );

        const icon =
            document.createElement("i");

        icon.className =
            type === "success"
                ? "fa-solid fa-circle-check"
                : "fa-solid fa-circle-exclamation";

        const text =
            document.createElement("span");

        text.textContent = message;

        messageElement.appendChild(icon);
        messageElement.appendChild(text);

        if (uploadBox) {

            uploadBox.insertAdjacentElement(
                "afterend",
                messageElement
            );

        }

        setTimeout(() => {

            if (messageElement.isConnected) {
                messageElement.remove();
            }

        }, 5000);
    }


    /* ==========================================
       Update Upload Title
    ========================================== */

    function updateUploadTitle(titleText) {

        if (!uploadLabel) {
            return;
        }

        const title =
            uploadLabel.querySelector("h3");

        if (title) {
            title.textContent = titleText;
        }
    }


    /* ==========================================
       Update File Information
    ========================================== */

    function updateFileInformation(file) {

        if (!fileName || !file) {
            return;
        }

        fileName.textContent = "";

        const icon =
            document.createElement("i");

        icon.className =
            "fa-solid fa-file-image";

        const name =
            document.createTextNode(
                ` ${file.name} `
            );

        const size =
            document.createElement("span");

        size.textContent =
            `(${formatFileSize(file.size)})`;

        fileName.appendChild(icon);
        fileName.appendChild(name);
        fileName.appendChild(size);
    }


    /* ==========================================
       Image Preview
    ========================================== */

    function previewFile(file) {

        if (!file || !previewImage) {
            return;
        }

        const reader =
            new FileReader();

        reader.onload = (event) => {

            if (!event.target?.result) {
                showMessage(
                    "Unable to preview this image."
                );

                return;
            }

            previewImage.src =
                event.target.result;

            previewImage.style.display =
                "block";
        };

        reader.onerror = () => {

            showMessage(
                "Unable to preview this image. Please try another file."
            );
        };

        reader.readAsDataURL(file);

        updateUploadTitle(
            "Image Selected"
        );

        updateFileInformation(file);
    }


    /* ==========================================
       Reset Preview
    ========================================== */

    function resetPreview() {

        if (imageInput) {
            imageInput.value = "";
        }

        if (previewImage) {

            previewImage.removeAttribute("src");

            previewImage.style.display =
                "none";
        }

        if (fileName) {

            fileName.textContent = "";

            const icon =
                document.createElement("i");

            icon.className =
                "fa-solid fa-image";

            fileName.appendChild(icon);

            fileName.appendChild(
                document.createTextNode(
                    " No file selected"
                )
            );
        }

        updateUploadTitle(
            "Select an Image"
        );

        if (uploadBox) {

            uploadBox.classList.remove(
                "drag-active"
            );
        }

        removeMessage();
    }


    /* ==========================================
       Validate Image
    ========================================== */

    function validateImage(file) {

        if (!file) {

            showMessage(
                "Please select an image first."
            );

            return false;
        }


        /* File Type */

        if (!ALLOWED_TYPES.has(file.type)) {

            showMessage(
                "Invalid file type. Please select JPG, JPEG, PNG, BMP or WEBP."
            );

            return false;
        }


        /* File Size */

        if (file.size > MAX_FILE_SIZE) {

            showMessage(
                "The selected image is larger than the 16 MB limit."
            );

            return false;
        }


        /* Empty File */

        if (file.size === 0) {

            showMessage(
                "The selected file is empty."
            );

            return false;
        }


        return true;
    }


    /* ==========================================
       File Input
    ========================================== */

    if (imageInput) {

        imageInput.addEventListener(
            "change",
            () => {

                const file =
                    imageInput.files?.[0];

                if (!file) {

                    resetPreview();

                    return;
                }

                if (!validateImage(file)) {

                    resetPreview();

                    return;
                }

                previewFile(file);
            }
        );
    }


    /* ==========================================
       Drag & Drop
    ========================================== */

    if (uploadBox) {

        uploadBox.addEventListener(
            "dragenter",
            (event) => {

                event.preventDefault();
                event.stopPropagation();

                uploadBox.classList.add(
                    "drag-active"
                );
            }
        );


        uploadBox.addEventListener(
            "dragover",
            (event) => {

                event.preventDefault();
                event.stopPropagation();

                uploadBox.classList.add(
                    "drag-active"
                );
            }
        );


        uploadBox.addEventListener(
            "dragleave",
            (event) => {

                event.preventDefault();
                event.stopPropagation();

                /*
                 * Only remove the active state when
                 * the pointer actually leaves the box.
                 */

                if (
                    !uploadBox.contains(
                        event.relatedTarget
                    )
                ) {

                    uploadBox.classList.remove(
                        "drag-active"
                    );
                }
            }
        );


        uploadBox.addEventListener(
            "drop",
            (event) => {

                event.preventDefault();
                event.stopPropagation();

                uploadBox.classList.remove(
                    "drag-active"
                );

                const file =
                    event.dataTransfer?.files?.[0];

                if (!file) {
                    return;
                }

                if (!validateImage(file)) {
                    return;
                }


                /*
                 * Assign dropped file to the
                 * actual file input.
                 */

                if (imageInput) {

                    try {

                        const dataTransfer =
                            new DataTransfer();

                        dataTransfer.items.add(file);

                        imageInput.files =
                            dataTransfer.files;

                    } catch (error) {

                        console.warn(
                            "Unable to assign dropped file to input:",
                            error
                        );
                    }
                }

                previewFile(file);
            }
        );
    }


    /* ==========================================
       Form Submission
    ========================================== */

    if (form) {

        form.addEventListener(
            "submit",
            (event) => {

                if (!imageInput) {

                    event.preventDefault();

                    showMessage(
                        "Image input could not be found."
                    );

                    return;
                }


                const file =
                    imageInput.files?.[0];


                /* Check file */

                if (!file) {

                    event.preventDefault();

                    showMessage(
                        "Please select an image before analyzing."
                    );

                    return;
                }


                /* Final validation */

                if (!validateImage(file)) {

                    event.preventDefault();

                    return;
                }


                /* Prevent double submission */

                if (
                    form.dataset.submitting === "true"
                ) {

                    event.preventDefault();

                    return;
                }

                form.dataset.submitting = "true";


                /* Disable submit button */

                const button =
                    form.querySelector(
                        "button[type='submit']"
                    );

                if (button) {

                    button.disabled = true;

                    button.setAttribute(
                        "aria-disabled",
                        "true"
                    );

                    button.innerHTML = `
                        <i class="fa-solid fa-spinner fa-spin"></i>
                        Analyzing...
                    `;
                }


                /* Show loading state */

                if (loading) {

                    loading.style.display =
                        "block";
                }
            }
        );
    }


    /* ==========================================
       Keyboard Accessibility
    ========================================== */

    if (uploadBox && imageInput) {

        uploadBox.addEventListener(
            "keydown",
            (event) => {

                if (
                    event.key === "Enter" ||
                    event.key === " "
                ) {

                    event.preventDefault();

                    imageInput.click();
                }
            }
        );
    }


    /* ==========================================
       Initial State
    ========================================== */

    if (previewImage) {

        previewImage.style.display =
            "none";
    }

});