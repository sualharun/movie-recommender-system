from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import pandas as pd
from fuzzywuzzy import fuzz, process

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Load model
try:
    with open('model.pkl', 'rb') as f:
        df, cosine_sim = pickle.load(f)
    print("Model loaded successfully!")
except FileNotFoundError:
    print("Model file not found. Please run train_recommender.py first.")
    df, cosine_sim = None, None

@app.route('/')
def home():
    return jsonify({
        "message": "Movie Recommendation API",
        "endpoints": {
            "/movies": "GET - Get all movies",
            "/recommend": "GET - Get recommendations (param: movie)",
            "/search": "GET - Search movies (param: query)"
        }
    })

def get_recommendations(title, cosine_sim=cosine_sim, df=df):
    """Get movie recommendations based on movie title with fuzzy matching"""
    if df is None or cosine_sim is None:
        return []
    
    # Try exact match first (case insensitive)
    exact_matches = df[df['title'].str.lower() == title.lower()]
    
    if len(exact_matches) > 0:
        idx = exact_matches.index[0]
        matched_title = df.iloc[idx]['title']
    else:
        # Use fuzzy matching to find the closest title
        all_titles = df['title'].tolist()
        best_match = process.extractOne(title, all_titles, scorer=fuzz.token_sort_ratio)
        
        # Lower the threshold from 60% to 40% for better matching
        if best_match and best_match[1] >= 40:
            matched_title = best_match[0]
            idx = df[df['title'] == matched_title].index[0]
        else:
            # Try partial matching as last resort
            partial_matches = df[df['title'].str.lower().str.contains(title.lower(), na=False)]
            if len(partial_matches) > 0:
                idx = partial_matches.index[0]
                matched_title = df.iloc[idx]['title']
            else:
                return []
    
    # Get the pairwise similarity scores
    sim_scores = list(enumerate(cosine_sim[idx]))
    
    # Sort movies based on similarity scores
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    
    # Get indices of the 10 most similar movies (excluding the input movie)
    movie_indices = [i[0] for i in sim_scores[1:11]]
    
    # Return the top 10 most similar movies
    recommendations = df.iloc[movie_indices][['title', 'genres', 'vote_average', 'release_date']].to_dict('records')
    
    # Include the matched title in the response
    return {
        'matched_title': matched_title,
        'recommendations': recommendations
    }

@app.route("/recommend", methods=["GET"])
def recommend():
    """Get movie recommendations"""
    movie_title = request.args.get('movie')
    
    if not movie_title:
        return jsonify({"error": "Movie parameter is required"}), 400
    
    result = get_recommendations(movie_title)
    
    if not result:
        # Provide suggestions for similar movie titles
        if df is not None:
            all_titles = df['title'].tolist()
            suggestions = process.extract(movie_title, all_titles, scorer=fuzz.token_sort_ratio, limit=5)
            suggestion_titles = [match[0] for match in suggestions if match[1] >= 30]
            
            return jsonify({
                "error": f"No movie found similar to '{movie_title}'",
                "suggestions": suggestion_titles[:3],  # Top 3 suggestions
                "message": "Try searching for one of these similar titles instead."
            }), 404
        else:
            return jsonify({"error": "Model not loaded"}), 500
    
    return jsonify({
        "input_movie": movie_title,
        "matched_movie": result['matched_title'],
        "recommendations": result['recommendations']
    })

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5001)
