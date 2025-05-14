/**
 * Show the photo modal with a given image URL and optional title
 * @param {string} imageUrl - The image to display
 * @param {string} [title] - Optional title
 */
function showPhotoModal(imageUrl, title = 'Photo View') {
  const modalImage = document.getElementById('modalImage');
  const modalTitle = document.getElementById('photoModalLabel');

  modalImage.src = imageUrl || '/static/logo.png';
  modalTitle.textContent = title;

  const photoModal = new bootstrap.Modal(document.getElementById('photoModal'));
  photoModal.show();
}
