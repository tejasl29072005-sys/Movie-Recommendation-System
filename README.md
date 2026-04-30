 🎬 Movie Recommendation System (Streamlit + ML)

A content-based movie recommendation system built using Machine Learning and deployed with Streamlit. The system suggests similar movies based on user-selected input using text similarity techniques.

🚀 Live Features

🎯 Search any movie from dataset
🧠 Content-based filtering using metadata
 📊 Cosine similarity for recommendations
🎨 Movie posters fetched using TMDB API
👍👎 Feedback buttons for interaction
⚡ Fast and interactive Streamlit UI

🧠 How It Works

The system recommends movies based on similarity of content features such as:

Overview
Genres
Keywords
Cast
Crew (Director)

Process Flow:

1. Load and merge TMDB datasets
2. Extract important features
3. Convert text data into numerical vectors using CountVectorizer
4. Compute similarity using Cosine Similarity
5. Recommend top 5 most similar movies


🛠️ Tech Stack

* Python 🐍
* Pandas
* Scikit-learn
* Streamlit
* NLP (Text Processing)
* TMDB API

📂 Dataset Used

TMDB 5000 Movies Dataset
 TMDB 5000 Credits Dataset


 ⚙️ Installation & Setup

1. Clone the repository

bash
git clone https://github.com/your-username/movie-recommender.git
cd movie-recommender

 2. Install dependencies

bash
pip install -r requirements.txt

 3. Run the Streamlit app

bash
streamlit run app.py

🔑 TMDB API Setup

This project uses TMDB API to fetch movie posters.

Replace the API key in the code:

python
API_KEY = "your_api_key_here"

Get your API key from: [https://www.themoviedb.org/](https://www.themoviedb.org/)


📸 Features Preview

Movie search dropdown
Recommended movies display
Poster images
Like / Dislike buttons

📌 Example

Input: Batman Begins
Output:

The Dark Knight
The Dark Knight Rises
Batman
Man of Steel
Batman Forever

 💡 Future Improvements

Add a user login system
Deploy on Streamlit Cloud
Improve recommendation using TF-IDF
Add rating-based hybrid recommender
Add a trending movies section


👨‍💻 Author

Tejas L
MCA Student | Data Science Enthusiast | DevOps Explorer | Machine Learning Developer


⭐ Show Support

If you like this project, give it a ⭐ on GitHub and share it!
