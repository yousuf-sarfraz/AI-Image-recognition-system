/* ==========================================
   Image & Text Recognition AI
   Frontend JavaScript
========================================== */

document.addEventListener("DOMContentLoaded", () => {

    const imageInput = document.getElementById("image");
    const previewImage = document.getElementById("preview-image");
    const uploadBox = document.querySelector(".upload-box");
    const uploadLabel = document.querySelector(".upload-box label");
    const fileName = document.getElementById("file-name");
    const form = document.querySelector("form");
    const loading = document.getElementById("loading");

    const MAX_SIZE = 16 * 1024 * 1024; // 16 MB

    const ALLOWED_TYPES = [
        "image/jpeg",
        "image/jpg",
        "image/png",
        "image/bmp",
        "image/webp"
    ];

    /* ==========================================
       Image Preview
    ========================================== */

    function previewFile(file) {

        if (!file) return;

        const reader = new FileReader();

        reader.onload = (e) => {

            previewImage.src = e.target.result;
            previewImage.style.display = "block";

        };

        reader.readAsDataURL(file);

        const title = uploadLabel.querySelector("h3");

        if (title) {
            title.textContent = "Image Selected";
        }

        if (fileName) {
            fileName.textContent = file.name;
        }

    }

    /* ==========================================
       Reset Preview
    ========================================== */

    function resetPreview() {

        imageInput.value = "";

        previewImage.src = "";
        previewImage.style.display = "none";

        if (fileName) {
            fileName.textContent = "No file selected";
        }

        const title = uploadLabel.querySelector("h3");

        if (title) {
            title.textContent = "Select an Image";
        }

    }

    /* ==========================================
       Validate Image
    ========================================== */

    function validateImage(file) {

        if (!ALLOWED_TYPES.includes(file.type)) {

            alert(
                "Only JPG, JPEG, PNG, BMP and WEBP images are allowed."
            );

            resetPreview();

            return false;

        }

        if (file.size > MAX_SIZE) {

            alert(
                "Maximum allowed file size is 16 MB."
            );

            resetPreview();

            return false;

        }

        return true;

    }

    /* ==========================================
       File Input
    ========================================== */

    if (imageInput) {

        imageInput.addEventListener("change", function () {

            const file = this.files[0];

            if (!file) {

                resetPreview();

                return;

            }

            if (!validateImage(file)) return;

            previewFile(file);

        });

    }

    /* ==========================================
       Drag & Drop
    ========================================== */

    if (uploadBox) {

        ["dragenter", "dragover"].forEach(event => {

            uploadBox.addEventListener(event, (e) => {

                e.preventDefault();

                uploadBox.classList.add("drag-active");

            });

        });

        ["dragleave", "dragend", "drop"].forEach(event => {

            uploadBox.addEventListener(event, (e) => {

                e.preventDefault();

                uploadBox.classList.remove("drag-active");

            });

        });

        uploadBox.addEventListener("drop", (e) => {

            const file = e.dataTransfer.files[0];

            if (!file) return;

            if (!validateImage(file)) return;

            imageInput.files = e.dataTransfer.files;

            previewFile(file);

        });

    }

    /* ==========================================
       Form Submission
    ========================================== */

    if (form) {

        form.addEventListener("submit", (e) => {

            if (!imageInput.files.length) {

                e.preventDefault();

                alert("Please select an image first.");

                return;

            }

            const button = form.querySelector("button");

            if (button) {

                button.disabled = true;

                button.innerHTML = `
                    <i class="fa-solid fa-spinner fa-spin"></i>
                    Analyzing...
                `;

            }

            if (loading) {

                loading.style.display = "block";

            }

        });

    }

});