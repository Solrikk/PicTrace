document.getElementById('upload-form').addEventListener('submit', async function(event) {
  event.preventDefault();

  const input = document.getElementById('file-input');
  const file = input.files[0];

  const formData = new FormData();
  formData.append('file', file);

  console.log("Uploading file...");
  const response = await fetch('/upload/', {
    method: 'POST',
    body: formData
  });

  const data = await response.json();
  console.log("File uploaded. Data received: ", data);
  displayResults(data);
});

function displayResults(data) {
  console.log("Displaying results...");
  const resultsDiv = document.getElementById('results');
  resultsDiv.innerHTML = `
      <h3>Uploaded Image:</h3>
      <div class="image-container">
          <img src="/uploads/${data.filename}.jpg" alt="Uploaded Image" class="uploaded-image"/>
      </div>
      <h3>Similar Images:</h3>
      <div class="similar-images-grid"></div>
  `;

  const grid = resultsDiv.querySelector('.similar-images-grid');
  data.similar_images.forEach(image_url => {
    console.log("Adding similar image: ", image_url);
    const imgElement = document.createElement('img');
    imgElement.src = image_url;
    imgElement.alt = "Similar Image";
    imgElement.classList.add('similar-image');
    grid.appendChild(imgElement);
  });
}
