const input = document.getElementById("id_image");
const preview = document.getElementById("beforePreview");
const sizeText = document.getElementById("beforeSize");

input.addEventListener("change", () => {
    const file = input.files[0];

    if (!file) return;

    // show preview
    preview.src = URL.createObjectURL(file);
    preview.style.display = "block";

    // calculate size
    const sizeMB = (file.size / (1024 * 1024)).toFixed(2);
    sizeText.innerText = `Size: ${sizeMB} MB`;
});