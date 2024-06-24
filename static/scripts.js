document.getElementById('upload-form').addEventListener('submit', async function(event) {
    event.preventDefault();

    const input = document.getElementById('file-input');
    const file = input.files[0];
    
    const formData = new FormData();
    formData.append('file', file);

    const response = await fetch('/upload/', {
        method: 'POST',
        body: formData
    });

    const data = await response.json();
    displayResults(data);
});

function displayResults(data) {
    const resultsDiv = document.getElementById('results');
    resultsDiv.innerHTML = `
        <h3>Uploaded Image:</h3>
        <img src="/uploads/${data.filename}" /><br>
        <h3>Similar Images:</h3>
    `;

    data.similar_images.forEach(image_url => {
        const imgElement = document.createElement('img');
        imgElement.src = image_url;
        resultsDiv.appendChild(imgElement);
    });
}