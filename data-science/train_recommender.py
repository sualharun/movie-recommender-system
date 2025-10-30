import pandas as pd
import pickle
import os
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer

def train_model():
    """Train the movie recommendation model"""
    print("Starting model training...")
    
    # Check if movies.csv exists
    if not os.path.exists("movies.csv"):
        print("Error: movies.csv not found!")
        print("Please download a movie dataset and place it as 'movies.csv'")
        return False
    
    try:
        # Load dataset
        print("Loading dataset...")
        df = pd.read_csv("movies.csv", low_memory=False)
        print(f"Loaded {len(df)} movies")
        print(f"Available columns: {list(df.columns)}")
        
        # Check for required columns and suggest alternatives
        required_columns = ['title', 'overview']
        available_columns = df.columns.tolist()
        
        # Map common column name variations
        column_mapping = {
            'overview': ['overview', 'plot', 'description', 'summary', 'storyline'],
            'title': ['title', 'movie_title', 'name'],
            'genres': ['genres', 'genre', 'categories'],
            'vote_average': ['vote_average', 'rating', 'imdb_rating', 'score'],
            'release_date': ['release_date', 'year', 'release_year']
        }
        
        # Find the best matching columns
        final_columns = {}
        for required, alternatives in column_mapping.items():
            found_column = None
            for alt in alternatives:
                if alt in available_columns:
                    found_column = alt
                    break
            
            if found_column:
                final_columns[required] = found_column
                print(f"Using '{found_column}' for {required}")
            else:
                print(f"Warning: No suitable column found for {required}")
        
        # Check if we have minimum required columns
        if 'title' not in final_columns or 'overview' not in final_columns:
            print("Error: Cannot find required 'title' and 'overview' columns")
            print("Please ensure your CSV has columns for movie titles and descriptions/plots")
            return False
        
        # Rename columns for consistency
        df_processed = df.rename(columns={
            final_columns.get('title'): 'title',
            final_columns.get('overview'): 'overview',
            final_columns.get('genres', 'genres'): 'genres',
            final_columns.get('vote_average', 'vote_average'): 'vote_average',
            final_columns.get('release_date', 'release_date'): 'release_date'
        })
        
        # Fill missing 'overview' with empty strings
        df_processed["overview"] = df_processed["overview"].fillna("").astype(str)
        
        # Remove movies with empty titles or overviews
        df_processed = df_processed[
            (df_processed['title'].notna()) & 
            (df_processed['title'] != '') &
            (df_processed['overview'] != '')
        ]
        
        print(f"Processing {len(df_processed)} movies after cleaning...")
        
        print("Creating TF-IDF vectors...")
        # TF-IDF Vectorization
        tfidf = TfidfVectorizer(
            stop_words="english",
            max_features=5000,  # Limit features for performance
            ngram_range=(1, 2)  # Include bigrams
        )
        tfidf_matrix = tfidf.fit_transform(df_processed["overview"])
        
        print("Computing similarity matrix...")
        # Compute similarity
        cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)
        
        print("Saving model...")
        # Save model
        with open("model.pkl", "wb") as f:
            pickle.dump((df_processed, cosine_sim), f)
        
        print(f"Training complete! Model saved with {len(df_processed)} movies.")
        print("Files created:")
        print("- model.pkl (trained model)")
        
        return True
        
    except Exception as e:
        print(f"Error during training: {str(e)}")
        return False

if __name__ == "__main__":
    success = train_model()
    if success:
        print("\n✅ Training completed successfully!")
    else:
        print("\n❌ Training failed!")
