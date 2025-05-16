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

function showAlertModal(id, title, warning, message, onConfirm) {
  document.getElementById(`${id}-title`).textContent = title;
  document.getElementById(`${id}-warning`).innerHTML = '<i class="fas fa-exclamation-triangle me-2"></i> ' + warning;
  document.getElementById(`${id}-message`).innerHTML = message;

  const confirmBtn = document.getElementById(`${id}-confirmBtn`);
  confirmBtn.onclick = function(e) {
    if (onConfirm) {
      e.preventDefault();
      onConfirm(e);
    }
  };

  const modal = new bootstrap.Modal(document.getElementById(id));
  modal.show();
}

