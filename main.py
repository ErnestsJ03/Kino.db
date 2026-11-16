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


    # Izveidot zanru tabulu.
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS genre(
            genre_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL UNIQUE
        )
    """)

    # Izveidot rezisoru tabulu.
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS director(
            director_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL
        )
    """)

    # Izveidot aktieru tabulu.
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS actor(
            actor_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL
        )
    """)

    # Pievienot zanra un rezisora ID filmu tabulai.
    movie_columns = [
        row[1] for row in cursor.execute(
            "PRAGMA table_info(movie)"
        ).fetchall()
    ]

    if "genre_id" not in movie_columns:
        cursor.execute("""
            ALTER TABLE movie ADD COLUMN genre_id INTEGER
            REFERENCES genre(genre_id)
        """)

    if "director_id" not in movie_columns:
        cursor.execute("""
            ALTER TABLE movie ADD COLUMN director_id INTEGER
            REFERENCES director(director_id)
        """)

    # Izveidot filmu un aktieru saistibas tabulu.
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS movie_actor(
            movie_id INTEGER,
            actor_id INTEGER,
            PRIMARY KEY(movie_id, actor_id),
            FOREIGN KEY(movie_id) REFERENCES movie(movie_id)
                ON DELETE CASCADE,
            FOREIGN KEY(actor_id) REFERENCES actor(actor_id)
                ON DELETE CASCADE
        )
    """)

    # Izveidot komentaru tabulu.
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS comments(
            comment_id INTEGER PRIMARY KEY,
            review_id INTEGER NOT NULL,
            user_id INTEGER NOT NULL,
            comment_text TEXT NOT NULL,
            FOREIGN KEY(review_id) REFERENCES reviews(review_id)
                ON DELETE CASCADE,
            FOREIGN KEY(user_id) REFERENCES users(user_id)
                ON DELETE CASCADE
        )
    """)

    # Izveidot skatamo filmu saraksta tabulu.
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS watchlist(
            watchlist_id INTEGER PRIMARY KEY,
            user_id INTEGER NOT NULL,
            movie_id INTEGER NOT NULL,
            UNIQUE(user_id, movie_id),
            FOREIGN KEY(user_id) REFERENCES users(user_id)
                ON DELETE CASCADE,
            FOREIGN KEY(movie_id) REFERENCES movie(movie_id)
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