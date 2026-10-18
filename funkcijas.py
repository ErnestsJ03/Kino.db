import sqlite3


# Pieslēgties datubāzei.
def connect():
    database = sqlite3.connect("Kino_skola.db")
    database.execute("PRAGMA foreign_keys = ON")
    return database


def add_movie(name):
    name = name.strip()

    if not name or len(name) > 200:
        raise ValueError(
            "Filmas nosaukumam vajag 1–200 rakstzīmes."
        )

    database = connect()

    try:
        cursor = database.cursor()

        cursor.execute(
            "INSERT INTO movie(title) VALUES (?)",
            (name,)
        )

        database.commit()
        movie_id = cursor.lastrowid

        return movie_id

    finally:
        database.close()


def add_user(name):
    name = name.strip()

    if not name or len(name) > 50:
        raise ValueError(
            "Lietotājvārdam vajag 1–50 rakstzīmes."
        )

    database = connect()

    try:
        cursor = database.cursor()

        cursor.execute(
            "INSERT INTO users(username) VALUES (?)",
            (name,)
        )

        database.commit()
        user_id = cursor.lastrowid

        return user_id

    finally:
        database.close()


def add_review(movie_id, user_id, rating, review):
    # Pārbaudīt skaitļus.
    try:
        movie_id = int(movie_id)
        user_id = int(user_id)
        rating = int(rating)

    except ValueError:
        raise ValueError(
            "ID un vērtējumam jābūt veseliem skaitļiem."
        )

    review = review.strip()

    if movie_id < 1 or user_id < 1:
        raise ValueError("ID jābūt lielākam par 0.")

    if rating < 1 or rating > 10:
        raise ValueError("Vērtējumam jābūt no 1 līdz 10.")

    if not review or len(review) > 2000:
        raise ValueError(
            "Atsauksmei vajag 1–2000 rakstzīmes."
        )

    database = connect()

    try:
        cursor = database.cursor()

        # Pārbaudīt, vai filma eksistē.
        cursor.execute(
            "SELECT movie_id FROM movie WHERE movie_id = ?",
            (movie_id,)
        )

        if cursor.fetchone() is None:
            raise ValueError("Filma ar šo ID nav atrasta.")

        # Pārbaudīt, vai lietotājs eksistē.
        cursor.execute(
            "SELECT user_id FROM users WHERE user_id = ?",
            (user_id,)
        )

        if cursor.fetchone() is None:
            raise ValueError("Lietotājs ar šo ID nav atrasts.")

        # Pievienot vērtējumu.
        cursor.execute("""
            INSERT OR IGNORE INTO rating(
                movie_id, user_id, rating
            )
            VALUES (?, ?, ?)
        """, (movie_id, user_id, rating))

        # Ja vērtējums jau bija, saglabāt jauno vērtību.
        cursor.execute("""
            UPDATE rating
            SET rating = ?
            WHERE movie_id = ? AND user_id = ?
        """, (rating, movie_id, user_id))

        # Pievienoju atsauksmi.
        cursor.execute("""
            INSERT OR IGNORE INTO reviews(
                movie_id, user_id, review
            )
            VALUES (?, ?, ?)
        """, (movie_id, user_id, review))

        # Ja atsauksme jau bija, saglabāt jauno tekstu.
        cursor.execute("""
            UPDATE reviews
            SET review = ?
            WHERE movie_id = ? AND user_id = ?
        """, (review, movie_id, user_id))

        database.commit()

    finally:
        database.close()


def get_movies(search=""):
    database = connect()

    try:
        cursor = database.cursor()

        cursor.execute("""
            SELECT
                movie.movie_id,
                movie.title,
                ROUND(AVG(rating.rating), 2),
                COUNT(rating.rating_id)

            FROM movie

            LEFT JOIN rating
            ON movie.movie_id = rating.movie_id

            WHERE movie.title LIKE ?

            GROUP BY movie.movie_id, movie.title
            ORDER BY movie.movie_id
        """, ("%" + search.strip() + "%",))

        movies = cursor.fetchall()

        return movies

    finally:
        database.close()


def get_users():
    database = connect()

    try:
        cursor = database.cursor()

        cursor.execute("""
            SELECT user_id, username
            FROM users
            ORDER BY user_id
        """)

        users = cursor.fetchall()

        return users

    finally:
        database.close()


def get_reviews():
    database = connect()

    try:
        cursor = database.cursor()

        cursor.execute("""
            SELECT
                movie.title,
                users.username,
                rating.rating,
                reviews.review

            FROM reviews

            JOIN movie
            ON reviews.movie_id = movie.movie_id

            JOIN users
            ON reviews.user_id = users.user_id

            LEFT JOIN rating
            ON reviews.movie_id = rating.movie_id
                AND reviews.user_id = rating.user_id

            ORDER BY reviews.review_id
        """)

        reviews = cursor.fetchall()

        return reviews

    finally:
        database.close()