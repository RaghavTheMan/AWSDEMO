function fetchMovieDetails() {
    const movieInput = document.getElementById('movie-input').value;
    if (!movieInput) {
        alert("Please enter a movie name!");
        return;
    }

    fetch(`http://127.0.0.1:5000/movie?name=${encodeURIComponent(movieInput)}`)
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert(data.error);
                return;
            }

            // Populate movie details
            document.getElementById('movie-poster').src = data.poster || "https://via.placeholder.com/150";
            document.getElementById('movie-title').textContent = data.title || "Title not available";
            document.getElementById('movie-release-date').textContent = `Release Date: ${data.release_date || "N/A"}`;
            document.getElementById('movie-overview').textContent = data.overview || "Overview not available.";
            document.getElementById('movie-review').textContent = data.top_review || "No reviews available.";

            document.getElementById('movie-details').classList.remove('hidden');
        })
        .catch(error => {
            console.error("Error fetching movie details:", error);
            alert("Something went wrong. Please try again!");
        });
}
