document.addEventListener('DOMContentLoaded', function() {
  const form = document.getElementById('upload-form');
  const fileInput = document.getElementById('file-input');
  const loadingElement = document.getElementById('loading');
  const resultsDiv = document.getElementById('results');

  form.addEventListener('submit', async function(event) {
    event.preventDefault();
    const file = fileInput.files[0];
    const formData = new FormData();
    formData.append('file', file);
    loadingElement.style.display = 'block';

    try {
      const response = await fetch('/find_similar/', {
        method: 'POST',
        body: formData
      });
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      const data = await response.json();
      displayResults(data);
    } catch (error) {
      console.error("Error uploading file: ", error);
    } finally {
      loadingElement.style.display = 'none';
    }
  });

  function displayResults(data) {
    resultsDiv.innerHTML = `
      <h3>Uploaded Image:</h3>
      <div class="image-container">
          <img src="/uploads/${encodeURIComponent(data.filename)}" alt="Uploaded Image" class="uploaded-image"/>
      </div>
      <h3>Similar Images:</h3>
      <div class="similar-images-grid"></div>
    `;
    const grid = resultsDiv.querySelector('.similar-images-grid');
    if (data.similar_images.length === 0) {
      grid.innerHTML = '<p>No similar images found.</p>';
    } else {
      data.similar_images.forEach(function(image_url) {
        const imgElement = document.createElement('img');
        imgElement.src = `/uploads/${encodeURIComponent(image_url)}`;
        imgElement.alt = "Similar Image";
        imgElement.classList.add('similar-image');
        grid.appendChild(imgElement);
      });
    }
  }
});
