# Movie Recommendation System

This project consists of two main components:
1. A Python-based movie recommendation engine
2. A Spring Boot web application

## Prerequisites

### System Requirements
- Python 3.10 (3.10 is needed to run this)
- Java 17
- Maven
- Node.js (for running the frontend server)
- npm (Node Package Manager)

### Python Dependencies
- pandas
- scikit-learn
- numpy
- flask
- flask-cors
- fuzzywuzzy (for fuzzy string matching)
- python-Levenshtein (for faster fuzzy matching)

### Java Dependencies
- Spring Boot 3.x
- Spring Web
- Spring Data JPA
- Lombok

### Frontend Dependencies
- http-server (can be installed globally via npm)

## Setup and Running

- need older version of python (BEFORE RUNNING DATA-SCIENCE)

brew install python@3.10
which python3.10
python3.10 --version

### Data Science Component (Python)

1. Navigate to the data-science directory:
   ```bash
   cd data-science
   ```

2. **Download the movie dataset:**
   
   **Option 1 - Kaggle Movies Dataset (Recommended):**
   - Go to [Kaggle's Movies Dataset](https://www.kaggle.com/datasets/rounakbanik/the-movies-dataset)
   - Download `movies_metadata.csv`
   - Rename it to `movies.csv` and place it in the `data-science/` directory
   
   **Option 2 - TMDB 5000 Movies (Alternative):**
   - Go to [TMDB 5000 Movie Dataset](https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata)
   - Download `tmdb_5000_movies.csv`
   - Rename it to `movies.csv`
   
   **Option 3 - IMDB Movies Dataset:**
   - Go to [IMDB Movies Dataset](https://www.kaggle.com/datasets/harshitshankhdhar/imdb-dataset-of-top-1000-movies-and-tv-shows)
   - Use any CSV with movie titles and descriptions
   
   **Required/Acceptable Column Names:**
   - **Title**: `title`, `movie_title`, `name`
   - **Description**: `overview`, `plot`, `description`, `summary`, `storyline`
   - **Genres**: `genres`, `genre`, `categories` (optional)
   - **Rating**: `vote_average`, `rating`, `imdb_rating`, `score` (optional)
   - **Year**: `release_date`, `year`, `release_year` (optional)

3. Create and activate a virtual environment:
   ```bash
   python3.10 -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```

4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   
   # If you encounter issues with fuzzywuzzy, install manually:
   pip install fuzzywuzzy python-Levenshtein
   ```

5. Train the recommendation model:
   ```bash
   python3.10 train_recommender.py
   ```
   This will create `model.pkl` from your `movies.csv` dataset.

6. Run the Flask server:
   ```bash
   python3.10 movie_recommender.py
   ```

The Flask server will be available at `http://localhost:5001`

### Spring Boot Component (Java)

1. From the root directory, run:
   ```bash
   ./mvnw spring-boot:run
   ```
   Or on Windows:
   ```bash
   mvnw.cmd spring-boot:run
   ```

The Spring Boot application will be available at `http://localhost:8080`

### Frontend

1. Install http-server globally:
   ```bash
   npm install -g http-server
   ```

2. Navigate to frontend directory and start the server:
   ```bash
   cd frontend
   http-server -p 3000
   ```

The application will be available at http://localhost:3000

## Testing the API

You can test the movie recommendation API using:
```
http://localhost:5001/recommend?movie=Inception
```

Example API calls:
```bash
# Test Flask API directly
curl "http://localhost:5001/recommend?movie=batman"
curl "http://localhost:5001/search?query=spider"

# Test through Spring Boot proxy
curl "http://localhost:8080/api/recommendations?movie=superman"
```

## GitHub Repository

This project is available at: [https://github.com/sualharun/movie-recommender-system](https://github.com/sualharun/movie-recommender-system)

## Project Structure

- `data-science/`: Contains the Python-based recommendation engine
  - `movie_recommender.py`: Flask server for recommendations
  - `train_recommender.py`: Script to train the recommendation model
  - `movies.csv`: Movie dataset (⚠️ **Download separately from Kaggle - not in repo due to size**)
  - `model.pkl`: Trained model file (generated after training)
  - `requirements.txt`: Python dependencies
- `src/`: Contains the Spring Boot application code
- `frontend/`: Contains the web interface
- `pom.xml`: Maven configuration
- `.gitignore`: Excludes large files from version control

## Important Notes

⚠️ **Dataset Required**: You must download `movies.csv` separately from Kaggle due to file size limitations on GitHub.

📋 **Flexible Column Names**: The system automatically detects various column name formats:
- Movie titles: `title`, `movie_title`, `name`
- Movie descriptions: `overview`, `plot`, `description`, `summary`
- The training script will show you which columns it found and used

🔧 **Dataset Compatibility**: Works with most movie datasets from Kaggle, IMDB, or TMDB as long as they have movie titles and descriptions.

🚀 **Features**:
- Fuzzy string matching for movie titles
- TF-IDF vectorization for content-based recommendations
- Microservices architecture with Flask and Spring Boot
- Responsive web interface

## Troubleshooting

- If `movies.csv` is missing, download it from Kaggle
- If `model.pkl` is missing, run `train_recommender.py` 
- If port 5001 is busy, disable AirPlay Receiver in System Settings
- For Java compilation errors, ensure Java 17 is being used