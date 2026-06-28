document.addEventListener('DOMContentLoaded', function() {
  const form = document.getElementById('upload-form');
  const fileInput = document.getElementById('file-input');
  const fileName = document.getElementById('file-name');
  const fileMeta = document.getElementById('file-meta');
  const filePreview = document.getElementById('file-preview');
  const loadingElement = document.getElementById('loading');
  const submitButton = document.getElementById('submit-button');
  const resultsDiv = document.getElementById('results');
  const gallery = document.getElementById('gallery');
  const galleryStatus = document.getElementById('gallery-status');
  const libraryCount = document.getElementById('library-count');
  const cacheCount = document.getElementById('cache-count');
  let previewUrl = null;

  fileInput.addEventListener('change', function() {
    const file = fileInput.files[0];

    if (previewUrl) {
      URL.revokeObjectURL(previewUrl);
      previewUrl = null;
    }

    if (!file) {
      fileName.textContent = 'Choose image';
      fileMeta.textContent = 'JPG, PNG, WebP';
      filePreview.hidden = true;
      filePreview.removeAttribute('src');
      return;
    }

    fileName.textContent = file.name;
    fileMeta.textContent = formatFileSize(file.size);
    previewUrl = URL.createObjectURL(file);
    filePreview.src = previewUrl;
    filePreview.hidden = false;
  });

  form.addEventListener('submit', async function(event) {
    event.preventDefault();
    const file = fileInput.files[0];

    if (!file) {
      showError('Choose an image first.');
      return;
    }

    const formData = new FormData();
    formData.append('file', file);
    setBusy(true);

    try {
      const response = await fetch('/find_similar/', {
        method: 'POST',
        body: formData
      });

      if (!response.ok) {
        throw new Error('Search request failed.');
      }

      const data = await response.json();

      if (data.error) {
        throw new Error(data.error);
      }

      displayResults(data);
      loadStats();
    } catch (error) {
      console.error('Error uploading file: ', error);
      showError(error.message || 'Search failed.');
    } finally {
      setBusy(false);
    }
  });

  function setBusy(isBusy) {
    submitButton.disabled = isBusy;
    submitButton.textContent = isBusy ? 'Searching' : 'Find matches';
    loadingElement.hidden = !isBusy;
  }

  function displayResults(data) {
    resultsDiv.innerHTML = '';

    const header = document.createElement('div');
    header.className = 'results-header';
    header.innerHTML = `
      <div>
        <p class="eyebrow">Results</p>
        <h2>Nearest matches</h2>
      </div>
      <span class="section-meta">${data.total_processed || 0} scanned</span>
    `;

    const layout = document.createElement('div');
    layout.className = 'result-layout';

    const uploadedCard = document.createElement('article');
    uploadedCard.className = 'uploaded-card';

    const uploadedLabel = document.createElement('span');
    uploadedLabel.textContent = 'Reference';

    const uploadedImage = document.createElement('img');
    uploadedImage.src = `/uploads/${encodeURIComponent(data.filename)}`;
    uploadedImage.alt = 'Uploaded image';
    uploadedImage.className = 'uploaded-image';

    uploadedCard.append(uploadedLabel, uploadedImage);

    const matchGrid = document.createElement('div');
    matchGrid.className = 'similar-images-grid';

    const matches = Array.isArray(data.similar_images) ? data.similar_images : [];

    if (matches.length === 0) {
      const empty = document.createElement('p');
      empty.textContent = 'No matches found.';
      matchGrid.appendChild(empty);
    } else {
      matches.forEach(function(imageInfo, index) {
        matchGrid.appendChild(createMatchCard(imageInfo, index + 1));
      });
    }

    layout.append(uploadedCard, matchGrid);
    resultsDiv.append(header, layout);
  }

  function createMatchCard(imageInfo, rank) {
    const card = document.createElement('article');
    card.className = 'match-card';

    const label = document.createElement('span');
    label.textContent = `Match ${rank}`;

    const imgElement = document.createElement('img');
    imgElement.src = `/uploads/${encodeURIComponent(imageInfo.filename)}`;
    imgElement.alt = 'Similar image';
    imgElement.className = 'similar-image';

    const scoreElement = document.createElement('div');
    scoreElement.className = 'similarity-score';
    scoreElement.textContent = `Score ${Number(imageInfo.similarity_score).toFixed(2)}`;

    card.append(label, imgElement, scoreElement);
    return card;
  }

  function showError(message) {
    resultsDiv.innerHTML = '';
    const error = document.createElement('div');
    error.className = 'error-state';
    error.textContent = message;
    resultsDiv.appendChild(error);
  }

  async function loadStats() {
    try {
      const response = await fetch('/cache_stats');
      const stats = await response.json();
      libraryCount.textContent = `${stats.total_images} images`;
      cacheCount.textContent = `${stats.cache_percentage}% cached`;
    } catch (error) {
      libraryCount.textContent = 'Library unavailable';
      cacheCount.textContent = 'Cache unavailable';
    }
  }

  async function loadGallery() {
    try {
      const response = await fetch('/gallery');
      const data = await response.json();
      const photos = Array.isArray(data.photos) ? data.photos : [];
      const fragment = document.createDocumentFragment();

      photos.forEach(function(photo) {
        const img = document.createElement('img');
        img.src = `/uploads/${encodeURIComponent(photo)}`;
        img.alt = 'Gallery image';
        img.loading = 'lazy';
        fragment.appendChild(img);
      });

      gallery.replaceChildren(fragment);
      galleryStatus.textContent = `${photos.length} shown`;
    } catch (error) {
      galleryStatus.textContent = 'Unavailable';
    }
  }

  function formatFileSize(bytes) {
    if (!bytes) {
      return '0 KB';
    }

    const units = ['B', 'KB', 'MB'];
    let size = bytes;
    let unitIndex = 0;

    while (size >= 1024 && unitIndex < units.length - 1) {
      size /= 1024;
      unitIndex += 1;
    }

    return `${size.toFixed(size >= 10 || unitIndex === 0 ? 0 : 1)} ${units[unitIndex]}`;
  }

  loadStats();
  loadGallery();
});
