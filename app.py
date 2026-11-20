
import sqlite3
import tkinter as tk
from tkinter import ttk

import main

from funkcijas import (
    add_movie,
    add_user,
    add_review,
    get_movies,
    get_users,
    get_reviews
)



# COLOUR SCHEME


BG = "#172337"
PANEL = "#22344D"
ACCENT = "#477DAF"
ACCENT_HOVER = "#38658F"
TEXT = "#E8EDF3"
MUTED = "#A8B5C5"
ENTRY_BG = "#F1F4F8"
OUTPUT_BG = "#111B2A"
SUCCESS = "#72C99A"
ERROR = "#F08080"

FONT = ("Arial", 10)
BOLD_FONT = ("Arial", 10, "bold")



# WINDOW

window = tk.Tk()
window.title("Kino datubāze")
window.geometry("1000x750")
window.minsize(800, 600)
window.configure(bg=BG)



# STYLES


style = ttk.Style()
style.theme_use("clam")

style.configure(
    "TNotebook",
    background=BG,
    borderwidth=0
)

style.configure(
    "TNotebook.Tab",
    background=PANEL,
    foreground=TEXT,
    padding=(13, 9),
    font=FONT
)

style.map(
    "TNotebook.Tab",
    background=[("selected", ACCENT)],
    foreground=[("selected", "white")]
)

style.configure("TFrame", background=BG)



# DESIGN FUNCTIONS


def create_label(parent, text):
    return tk.Label(
        parent,
        text=text,
        bg=BG,
        fg=TEXT,
        font=FONT
    )


def create_entry(parent):
    return tk.Entry(
        parent,
        font=FONT,
        bg=ENTRY_BG,
        fg="#172337",
        insertbackground="#172337",
        relief="flat",
        bd=0
    )


def create_button(parent, text, command):
    return tk.Button(
        parent,
        text=text,
        command=command,
        bg=ACCENT,
        fg="white",
        activebackground=ACCENT_HOVER,
        activeforeground="white",
        font=BOLD_FONT,
        relief="flat",
        bd=0,
        padx=15,
        pady=7,
        cursor="hand2"
    )


def create_block(parent, title):
    block = tk.LabelFrame(
        parent,
        text=title,
        bg=BG,
        fg=TEXT,
        font=BOLD_FONT,
        padx=20,
        pady=15,
        bd=1,
        relief="groove"
    )

    block.pack(fill="x", padx=25, pady=20)
    return block


def create_form(parent, title, fields, buttons):
    block = create_block(parent, title)
    entries = {}

    for label_text, variable_name in fields:
        create_label(
            block,
            label_text
        ).pack(anchor="w", pady=(8, 3))

        entry = create_entry(block)
        entry.pack(fill="x", ipady=7, pady=3)

        entries[variable_name] = entry

    for button_text, command in buttons:
        create_button(
            block,
            button_text,
            command
        ).pack(anchor="w", pady=(8, 2))

    return entries



# DATABASE FUNCTIONS


def connect_database():
    database = sqlite3.connect("Kino_skola.db")
    database.execute("PRAGMA foreign_keys = ON")
    return database


def get_table_data(query, parameters=()):
    database = connect_database()

    try:
        cursor = database.cursor()
        cursor.execute(query, parameters)
        return cursor.fetchall()
    finally:
        database.close()


def insert_data(query, parameters):
    database = connect_database()

    try:
        cursor = database.cursor()
        cursor.execute(query, parameters)
        database.commit()
    finally:
        database.close()


def show_data(title, rows):
    output.delete("1.0", tk.END)
    output.insert(tk.END, title + "\n")
    output.insert(tk.END, "-" * 80 + "\n")

    if not rows:
        output.insert(tk.END, "Nav atrasti dati.\n")
        return

    for row in rows:
        output.insert(tk.END, str(row) + "\n")


def show_message(message, color=SUCCESS):
    result.config(text=message, fg=color)


def add_simple_record(
    input_widget,
    query,
    success_message,
    error_message,
    show_function
):
    name = input_widget.get().strip()

    if not name:
        show_message("Lūdzu, aizpildiet ievades lauku.", ERROR)
        return

    try:
        insert_data(query, (name,))
        input_widget.delete(0, tk.END)

        show_message(success_message)
        show_function()

    except sqlite3.IntegrityError:
        show_message(error_message, ERROR)

    except sqlite3.Error as error:
        show_message(str(error), ERROR)



# MOVIES


def addFromWindow():
    name = movie_input.get().strip()

    try:
        movie_id = add_movie(name)
        movie_input.delete(0, tk.END)

        show_message(
            "Filma pievienota. ID: " + str(movie_id)
        )
        showMovies()

    except ValueError as error:
        show_message(str(error), ERROR)

    except sqlite3.IntegrityError:
        show_message("Šāda filma jau ir pievienota.", ERROR)


def showMovies():
    movies = get_movies(movie_input.get())

    show_data(
        "ID | Filma | Vidējais vērtējums | Vērtējumu skaits",
        movies
    )



# USERS


def addFromWindow2():
    name = user_input.get().strip()

    try:
        user_id = add_user(name)
        user_input.delete(0, tk.END)

        show_message(
            "Lietotājs pievienots. ID: " + str(user_id)
        )
        showUsers()

    except ValueError as error:
        show_message(str(error), ERROR)

    except sqlite3.IntegrityError:
        show_message("Šāds lietotājs jau ir pievienots.", ERROR)


def showUsers():
    show_data("ID | Lietotājvārds", get_users())



# REVIEWS


def addFromWindow3():
    try:
        add_review(
            movie_id_input.get(),
            user_id_input.get(),
            rating_input.get(),
            review_input.get()
        )

        show_message("Vērtējums un atsauksme saglabāti.")
        showReviews()

    except ValueError as error:
        show_message(str(error), ERROR)

    except sqlite3.IntegrityError:
        show_message(
            "Pārbaudiet filmas un lietotāja ID.",
            ERROR
        )


def showReviews():
    show_data(
        "Filma | Lietotājs | Vērtējums | Atsauksme",
        get_reviews()
    )


# =====================================
# GENRES
# =====================================

def addGenre():
    add_simple_record(
        genre_input,
        "INSERT INTO genre(name) VALUES (?)",
        "Žanrs pievienots.",
        "Šāds žanrs jau eksistē.",
        showGenres
    )


def showGenres():
    show_data(
        "ID | Žanrs",
        get_table_data("SELECT * FROM genre")
    )


# DIRECTORS


def addDirector():
    add_simple_record(
        director_input,
        "INSERT INTO director(name) VALUES (?)",
        "Režisors pievienots.",
        "Šāds režisors jau eksistē.",
        showDirectors
    )


def showDirectors():
    show_data(
        "ID | Režisors",
        get_table_data("SELECT * FROM director")
    )


# =====================================
# ACTORS
# =====================================

def addActor():
    add_simple_record(
        actor_input,
        "INSERT INTO actor(name) VALUES (?)",
        "Aktieris pievienots.",
        "Šāds aktieris jau eksistē.",
        showActors
    )


def showActors():
    show_data(
        "ID | Aktieris",
        get_table_data("SELECT * FROM actor")
    )


# =====================================
# MOVIE ACTORS
# =====================================

def addMovieActor():
    movie_id = movie_actor_movie_input.get().strip()
    actor_id = movie_actor_actor_input.get().strip()

    if not movie_id or not actor_id:
        show_message("Aizpildiet abus ID laukus.", ERROR)
        return

    try:
        insert_data(
            """
            INSERT INTO movie_actor(movie_id, actor_id)
            VALUES (?, ?)
            """,
            (movie_id, actor_id)
        )

        show_message("Aktieris pievienots filmai.")
        showMovieActors()

    except sqlite3.IntegrityError:
        show_message("Pārbaudiet filmu un aktiera ID.", ERROR)

    except sqlite3.Error as error:
        show_message(str(error), ERROR)


def showMovieActors():
    show_data(
        "Filmas ID | Aktiera ID",
        get_table_data("SELECT * FROM movie_actor")
    )


# =====================================
# COMMENTS
# =====================================

def addComment():
    review_id = comment_review_input.get().strip()
    user_id = comment_user_input.get().strip()
    comment = comment_input.get().strip()

    if not review_id or not user_id or not comment:
        show_message("Aizpildiet visus laukus.", ERROR)
        return

    try:
        insert_data(
            """
            INSERT INTO comments(
                review_id, user_id, comment_text
            )
            VALUES (?, ?, ?)
            """,
            (review_id, user_id, comment)
        )

        comment_input.delete(0, tk.END)
        show_message("Komentārs pievienots.")
        showComments()

    except sqlite3.IntegrityError:
        show_message(
            "Pārbaudiet atsauksmes un lietotāja ID.",
            ERROR
        )

    except sqlite3.Error as error:
        show_message(str(error), ERROR)


def showComments():
    show_data(
        "ID | Atsauksmes ID | Lietotāja ID | Komentārs",
        get_table_data("SELECT * FROM comments")
    )


# =====================================
# WATCHLIST
# =====================================

def addWatchlist():
    user_id = watch_user_input.get().strip()
    movie_id = watch_movie_input.get().strip()

    if not user_id or not movie_id:
        show_message("Aizpildiet abus ID laukus.", ERROR)
        return

    try:
        insert_data(
            """
            INSERT INTO watchlist(user_id, movie_id)
            VALUES (?, ?)
            """,
            (user_id, movie_id)
        )

        show_message(
            "Filma pievienota skatāmo filmu sarakstam."
        )
        showWatchlist()

    except sqlite3.IntegrityError:
        show_message(
            "Filma jau ir sarakstā vai ID nav pareizs.",
            ERROR
        )

    except sqlite3.Error as error:
        show_message(str(error), ERROR)


def showWatchlist():
    show_data(
        "ID | Lietotāja ID | Filmas ID",
        get_table_data("SELECT * FROM watchlist")
    )

# =====================================
# HEADER
# =====================================

header = tk.Label(
    window,
    text="KINO DATUBĀZE",
    font=("Arial", 21, "bold"),
    bg=BG,
    fg=TEXT
)

header.pack(pady=(15, 3))

subtitle = tk.Label(
    window,
    text="Filmu, lietotāju un atsauksmju pārvaldība",
    font=FONT,
    bg=BG,
    fg=MUTED
)

subtitle.pack(pady=(0, 12))


# =====================================
# TABS
# =====================================

tabs = ttk.Notebook(window)
tabs.pack(fill="both", expand=True, padx=20, pady=5)

movie_tab = ttk.Frame(tabs)
user_tab = ttk.Frame(tabs)
review_tab = ttk.Frame(tabs)
genre_tab = ttk.Frame(tabs)
director_tab = ttk.Frame(tabs)
actor_tab = ttk.Frame(tabs)
movie_actor_tab = ttk.Frame(tabs)
comment_tab = ttk.Frame(tabs)
watchlist_tab = ttk.Frame(tabs)

tabs.add(movie_tab, text="Filmas")
tabs.add(user_tab, text="Lietotāji")
tabs.add(review_tab, text="Atsauksmes")
tabs.add(genre_tab, text="Žanri")
tabs.add(director_tab, text="Režisori")
tabs.add(actor_tab, text="Aktieri")
tabs.add(movie_actor_tab, text="Filmu aktieri")
tabs.add(comment_tab, text="Komentāri")
tabs.add(watchlist_tab, text="Skatāmo filmu saraksts")


# =====================================
# MOVIES TAB
# =====================================

movie_fields = create_form(
    movie_tab,
    "Filmu pārvaldība",
    [
        ("Filmas nosaukums", "movie_input")
    ],
    [
        ("+ Pievienot filmu", addFromWindow),
        ("Rādīt / meklēt filmas", showMovies)
    ]
)

movie_input = movie_fields["movie_input"]


# =====================================
# USERS TAB
# =====================================

user_fields = create_form(
    user_tab,
    "Lietotāju pārvaldība",
    [
        ("Lietotājvārds", "user_input")
    ],
    [
        ("+ Pievienot lietotāju", addFromWindow2),
        ("Rādīt lietotājus", showUsers)
    ]
)

user_input = user_fields["user_input"]


# =====================================
# REVIEWS TAB
# =====================================

review_fields = create_form(
    review_tab,
    "Vērtējumi un atsauksmes",
    [
        ("Filmas ID", "movie_id_input"),
        ("Lietotāja ID", "user_id_input"),
        ("Vērtējums (1–10)", "rating_input"),
        ("Atsauksme", "review_input")
    ],
    [
        ("+ Saglabāt atsauksmi", addFromWindow3),
        ("Rādīt atsauksmes", showReviews)
    ]
)

movie_id_input = review_fields["movie_id_input"]
user_id_input = review_fields["user_id_input"]
rating_input = review_fields["rating_input"]
review_input = review_fields["review_input"]


# =====================================
# GENRES TAB
# =====================================

genre_fields = create_form(
    genre_tab,
    "Žanru pārvaldība",
    [
        ("Žanra nosaukums", "genre_input")
    ],
    [
        ("+ Pievienot žanru", addGenre),
        ("Rādīt žanrus", showGenres)
    ]
)

genre_input = genre_fields["genre_input"]


# =====================================
# DIRECTORS TAB
# =====================================

director_fields = create_form(
    director_tab,
    "Režisoru pārvaldība",
    [
        ("Režisora vārds", "director_input")
    ],
    [
        ("+ Pievienot režisoru", addDirector),
        ("Rādīt režisorus", showDirectors)
    ]
)

director_input = director_fields["director_input"]


# =====================================
# ACTORS TAB
# =====================================

actor_fields = create_form(
    actor_tab,
    "Aktieru pārvaldība",
    [
        ("Aktiera vārds", "actor_input")
    ],
    [
        ("+ Pievienot aktieri", addActor),
        ("Rādīt aktierus", showActors)
    ]
)

actor_input = actor_fields["actor_input"]


# =====================================
# MOVIE ACTORS TAB
# =====================================

movie_actor_fields = create_form(
    movie_actor_tab,
    "Pievienot aktieri filmai",
    [
        ("Filmas ID", "movie_actor_movie_input"),
        ("Aktiera ID", "movie_actor_actor_input")
    ],
    [
        ("+ Pievienot aktieri filmai", addMovieActor),
        ("Rādīt filmu aktierus", showMovieActors)
    ]
)

movie_actor_movie_input = movie_actor_fields[
    "movie_actor_movie_input"
]

movie_actor_actor_input = movie_actor_fields[
    "movie_actor_actor_input"
]


# =====================================
# COMMENTS TAB
# =====================================

comment_fields = create_form(
    comment_tab,
    "Komentāru pārvaldība",
    [
        ("Atsauksmes ID", "comment_review_input"),
        ("Lietotāja ID", "comment_user_input"),
        ("Komentārs", "comment_input")
    ],
    [
        ("+ Pievienot komentāru", addComment),
        ("Rādīt komentārus", showComments)
    ]
)

comment_review_input = comment_fields[
    "comment_review_input"
]

comment_user_input = comment_fields[
    "comment_user_input"
]

comment_input = comment_fields[
    "comment_input"
]


# =====================================
# WATCHLIST TAB
# =====================================

watchlist_fields = create_form(
    watchlist_tab,
    "Skatāmo filmu saraksts",
    [
        ("Lietotāja ID", "watch_user_input"),
        ("Filmas ID", "watch_movie_input")
    ],
    [
        ("+ Pievienot filmu sarakstam", addWatchlist),
        ("Rādīt skatāmo filmu sarakstu", showWatchlist)
    ]
)

watch_user_input = watchlist_fields[
    "watch_user_input"
]

watch_movie_input = watchlist_fields[
    "watch_movie_input"
]


# =====================================
# STATUS MESSAGE
# =====================================

result = tk.Label(
    window,
    text="Gatavs darbam!",
    bg=BG,
    fg=SUCCESS,
    font=FONT
)

result.pack(pady=5)


# =====================================
# OUTPUT AREA
# =====================================

output = tk.Text(
    window,
    width=100,
    height=10,
    bg=OUTPUT_BG,
    fg=TEXT,
    insertbackground=TEXT,
    font=("Consolas", 10),
    relief="flat",
    bd=0,
    padx=12,
    pady=10,
    selectbackground=ACCENT
)

output.pack(
    fill="both",
    padx=20,
    pady=(5, 15)
)


# =====================================
# START APPLICATION
# =====================================

showMovies()

window.mainloop()
