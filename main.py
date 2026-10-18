import sqlite3

# Pieslēgties datubāzei.
database = sqlite3.connect("Kino_skola.db")
cursor = database.cursor()
database.execute("PRAGMA foreign_keys = ON")

try:
    # Izveidot filmu tabulu.
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS movie(
            movie_id INTEGER PRIMARY KEY,
            title TEXT NOT NULL UNIQUE
        )
    """)

    # Izveidot lietotāju tabulu.
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users(
            user_id INTEGER PRIMARY KEY,
            username TEXT NOT NULL UNIQUE
        )
    """)

    # Izveidot vērtējumu tabulu.
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS rating(
            rating_id INTEGER PRIMARY KEY,
            movie_id INTEGER NOT NULL,
            user_id INTEGER NOT NULL,
            rating INTEGER NOT NULL CHECK(rating BETWEEN 1 AND 10),
            UNIQUE(movie_id, user_id),
            FOREIGN KEY(movie_id) REFERENCES movie(movie_id)
                ON DELETE CASCADE,
            FOREIGN KEY(user_id) REFERENCES users(user_id)
                ON DELETE CASCADE
        )
    """)

    # Izveidot atsauksmju tabulu.
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS reviews(
            review_id INTEGER PRIMARY KEY,
            movie_id INTEGER NOT NULL,
            user_id INTEGER NOT NULL,
            review TEXT NOT NULL,
            UNIQUE(movie_id, user_id),
            FOREIGN KEY(movie_id) REFERENCES movie(movie_id)
                ON DELETE CASCADE,
            FOREIGN KEY(user_id) REFERENCES users(user_id)
                ON DELETE CASCADE
        )
    """)

    # Pievienot filmas.
    cursor.execute("""
        INSERT OR IGNORE INTO movie(movie_id, title)
        VALUES (1, 'A Bronx Tale')
    """)

    cursor.execute("""
        INSERT OR IGNORE INTO movie(movie_id, title)
        VALUES (2, 'The Godfather')
    """)

    cursor.execute("""
        INSERT OR IGNORE INTO movie(movie_id, title)
        VALUES (3, 'The Shawshank Redemption')
    """)

    # Pievienot lietotājus.
    cursor.execute("""
        INSERT OR IGNORE INTO users(user_id, username)
        VALUES (1, 'Aleksandrs')
    """)

    cursor.execute("""
        INSERT OR IGNORE INTO users(user_id, username)
        VALUES (2, 'Janis')
    """)

    cursor.execute("""
        INSERT OR IGNORE INTO users(user_id, username)
        VALUES (3, 'Viktors')
    """)

    # Pievienot vērtējumus.
    cursor.execute("""
        INSERT OR IGNORE INTO rating(
            rating_id, movie_id, user_id, rating
        )
        VALUES (1, 1, 1, 9)
    """)

    cursor.execute("""
        INSERT OR IGNORE INTO rating(
            rating_id, movie_id, user_id, rating
        )
        VALUES (2, 2, 2, 10)
    """)

    cursor.execute("""
        INSERT OR IGNORE INTO rating(
            rating_id, movie_id, user_id, rating
        )
        VALUES (3, 3, 3, 10)
    """)

    # Pievienot atsauksmes.
    cursor.execute("""
        INSERT OR IGNORE INTO reviews(
            review_id, movie_id, user_id, review
        )
        VALUES (1, 1, 1, 'Great movie with a complex plot.')
    """)

    cursor.execute("""
        INSERT OR IGNORE INTO reviews(
            review_id, movie_id, user_id, review
        )
        VALUES (2, 2, 2, 'A masterpiece of cinema.')
    """)

    cursor.execute("""
        INSERT OR IGNORE INTO reviews(
            review_id, movie_id, user_id, review
        )
        VALUES (3, 3, 3, 'A story of hope and friendship.')
    """)

    database.commit()

finally:
    database.close()