function copyToClipboard() {
    const messageBox = document.querySelector('.message-box');
    if (messageBox) {
        const text = messageBox.innerText;
        navigator.clipboard.writeText(text).then(() => {
            alert('Message copied to clipboard!');
        }).catch(err => {
            console.error('Failed to copy:', err);
        });
    }
}

document.addEventListener('DOMContentLoaded', function() {
    const fileInputs = document.querySelectorAll('input[type="file"]');
    fileInputs.forEach(input => {
        input.addEventListener('change', function() {
            const fileName = this.files[0].name;
            const label = this.previousElementSibling;
            if (label) {
                label.innerText = `Selected: ${fileName}`;
            }
        });
    });
});