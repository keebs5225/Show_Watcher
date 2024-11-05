document.addEventListener('DOMContentLoaded', (event) => {
  // Prevent default context menu and open edit modal on right-click
  document.querySelectorAll('.list-group-item').forEach((item) => {
    item.addEventListener('contextmenu', function (e) {
      e.preventDefault();
      const showId = this.getAttribute('data-show-id');
      openEditModal(showId);
    });
  });
});

function openEditModal(showId) {
  window.location.href = `/edit-show/${showId}`;
}

function toggleAddShowForm() {
  const form = document.getElementById("add-show-form");
  form.style.display = form.style.display === "none" ? "block" : "none";
}

// Sorting function to sort shows based on criteria and order
function sortShowsBy(criteria, order) {
  const list = document.getElementById("watchlist");
  const items = Array.from(list.getElementsByTagName("li"));

  items.sort((a, b) => {
    let aValue, bValue;

    // Retrieve values based on the sorting criteria
    switch (criteria) {
      case "title":
        aValue = a.getAttribute("data-title").toLowerCase();
        bValue = b.getAttribute("data-title").toLowerCase();
        break;
      case "genre":
        aValue = a.getAttribute("data-genre").toLowerCase();
        bValue = b.getAttribute("data-genre").toLowerCase();
        break;
      case "release_year":
        aValue = parseInt(a.getAttribute("data-release-year"), 10);
        bValue = parseInt(b.getAttribute("data-release-year"), 10);
        break;
      case "rating":
        aValue = parseFloat(a.getAttribute("data-rating"));
        bValue = parseFloat(b.getAttribute("data-rating"));
        break;
      default:
        return 0;
    }

    // Compare values for sorting
    if (aValue < bValue) return order === "asc" ? -1 : 1;
    if (aValue > bValue) return order === "asc" ? 1 : -1;
    return 0;
  });

  // Clear and re-add sorted items
  list.innerHTML = "";
  items.forEach((item) => list.appendChild(item));
}

// Event listener for sorting dropdown
document.getElementById("sort-dropdown").addEventListener("change", (e) => {
  const [criteria, order] = e.target.value.split("-");
  sortShowsBy(criteria, order);
});
