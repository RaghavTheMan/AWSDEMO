from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend-backend communication

TMDB_API_KEY = '0d1c38a77122f7212cc19086b9fbbdfa'  # Replace with your TMDb API key

@app.route('/movie', methods=['GET'])
def get_movie():
    movie_name = request.args.get('name')
    if not movie_name:
        return jsonify({'error': 'Missing movie name'}), 400

    try:
        # Fetch movie details from TMDb
        tmdb_url = f"https://api.themoviedb.org/3/search/movie?api_key={TMDB_API_KEY}&query={movie_name}"
        tmdb_response = requests.get(tmdb_url)
        tmdb_data = tmdb_response.json()

        if 'results' not in tmdb_data or not tmdb_data['results']:
            return jsonify({'error': 'No movie found'}), 404

        # Get the first movie in the results
        movie = tmdb_data['results'][0]
        movie_id = movie.get('id')
        movie_details = {
            'title': movie.get('title', 'N/A'),
            'poster': f"https://image.tmdb.org/t/p/w500{movie.get('poster_path')}" if movie.get('poster_path') else None,
            'overview': movie.get('overview', 'No overview available'),
            'release_date': movie.get('release_date', 'Unknown')  # Ensure the release date is handled
        }

        # Fetch reviews from TMDb
        reviews_url = f"https://api.themoviedb.org/3/movie/{movie_id}/reviews?api_key={TMDB_API_KEY}"
        reviews_response = requests.get(reviews_url)
        reviews_data = reviews_response.json()

        # Get the first review (if available)
        if 'results' in reviews_data and reviews_data['results']:
            top_review = reviews_data['results'][0]
            movie_details['review'] = top_review.get('content', 'No review content available')
        else:
            movie_details['review'] = "No reviews available for this movie"

        return jsonify(movie_details)

    except Exception as e:
        return jsonify({'error': 'Something went wrong. Please try again!', 'details': str(e)}), 500


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
