
from flask import Flask, render_template, request

app = Flask(__name__)

# Sample dataset for the college project
GAMES = [
    {"name": "GTA V", "genre": "Action",
     "platform": "PC", "rating": 9.0},
    {"name": "Red Dead Redemption 2", "genre": "Adventure",
     "platform": "PC", "rating": 9.5},
    {"name": "Minecraft", "genre": "Sandbox",
     "platform": "PC", "rating": 9.0},
    {"name": "FIFA 25", "genre": "Sports",
     "platform": "PlayStation", "rating": 8.0},
    {"name": "God of War", "genre": "Action",
     "platform": "PlayStation", "rating": 9.2},
    {"name": "Forza Horizon 5", "genre": "Racing",
     "platform": "Xbox", "rating": 8.8},
    {"name": "The Legend of Zelda", "genre": "Adventure",
     "platform": "Nintendo", "rating": 9.7},
    {"name": "Stardew Valley", "genre": "Simulation",
     "platform": "PC", "rating": 8.9},
    {"name": "Rocket League", "genre": "Sports",
     "platform": "PC", "rating": 8.5},
    {"name": "Cyberpunk 2077", "genre": "RPG",
     "platform": "PC", "rating": 8.6},
]


def recommend_games(genre, platform, min_rating):
    results = []

    for game in GAMES:
        genre_match = (
            genre == "All" or game["genre"] == genre
        )
        platform_match = (
            platform == "All"
            or game["platform"] == platform
        )
        rating_match = game["rating"] >= min_rating

        if genre_match and platform_match and rating_match:
            results.append(game)

    return sorted(
        results,
        key=lambda game: game["rating"],
        reverse=True
    )


@app.route("/", methods=["GET", "POST"])
def home():
    recommendations = []
    searched = False

    genre = "All"
    platform = "All"
    min_rating = 0.0
    error = None

    if request.method == "POST":
        searched = True
        genre = request.form.get("genre", "All")
        platform = request.form.get("platform", "All")

        try:
            min_rating = float(request.form.get("min_rating", 0))
            if not 0 <= min_rating <= 10:
                raise ValueError
        except ValueError:
            error = "Enter a rating between 0 and 10."

        if error is None:
            recommendations = recommend_games(
                genre, platform, min_rating
            )

    return render_template(
        "index.html",
        games=recommendations,
        searched=searched,
        genre=genre,
        platform=platform,
        min_rating=min_rating,
        error=error
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
