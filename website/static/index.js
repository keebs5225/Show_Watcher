function deleteNote(noteId) {
  fetch("/delete-note", {
    method: "POST",
    body: JSON.stringify({ noteId: noteId }),
  }).then((_res) => {
    window.location.href = "/";
  });
}

document.addEventListener('DOMContentLoaded', (event) => {
  // Disable default context menu on the list-group items
  document.querySelectorAll('.list-group-item').forEach((item) => {
    item.addEventListener('contextmenu', function (e) {
      e.preventDefault(); // Prevent the default right-click menu

      const showId = this.querySelector('.context-menu').getAttribute('data-show-id');
      openEditModal(showId);  // Call the function to open the edit modal
    });
  });
});

// Function to open the edit modal or redirect to edit page
function openEditModal(showId) {
  // You can replace this with your modal logic
  // For now, redirect to the edit-show page
  window.location.href = `/edit-show/${showId}`;
}
