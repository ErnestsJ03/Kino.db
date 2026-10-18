import sqlite3
import tkinter as tk
from tkinter import ttk

# Izveido tabulas un pievieno paraugdatus.
import main

from funkcijas import (
    add_movie,
    add_user,
    add_review,
    get_movies,
    get_users,
    get_reviews
)


def addFromWindow():
    name = movie_input.get()

    try:
        movie_id = add_movie(name)

        movie_input.delete(0, tk.END)

        result.config(
            text="Filma pievienota. ID: " + str(movie_id),
            fg="green"
        )

        showMovies()

    except ValueError as error:
        result.config(text=str(error), fg="red")

    except sqlite3.IntegrityError:
        result.config(
            text="Šāda filma jau ir pievienota.",
            fg="red"
        )


def addFromWindow2():
    name = user_input.get()

    try:
        user_id = add_user(name)

        user_input.delete(0, tk.END)

        result.config(
            text="Lietotājs pievienots. ID: " + str(user_id),
            fg="green"
        )

        showUsers()

    except ValueError as error:
        result.config(text=str(error), fg="red")

    except sqlite3.IntegrityError:
        result.config(
            text="Šāds lietotājs jau ir pievienots.",
            fg="red"
        )


def addFromWindow3():
    movie_id = movie_id_input.get()
    user_id = user_id_input.get()
    rating = rating_input.get()
    review = review_input.get()

    try:
        add_review(movie_id, user_id, rating, review)

        result.config(
            text="Vērtējums un atsauksme saglabāti.",
            fg="green"
        )

        showReviews()

    except ValueError as error:
        result.config(text=str(error), fg="red")

    except sqlite3.IntegrityError:
        result.config(
            text="Pārbaudiet filmas un lietotāja ID.",
            fg="red"
        )


def showMovies():
    output.delete("1.0", tk.END)
    output.insert(
        tk.END,
        "ID | Filma | Vidējais | Vērtējumu skaits\n"
    )

    for movie in get_movies(movie_input.get()):
        output.insert(tk.END, str(movie) + "\n")


def showUsers():
    output.delete("1.0", tk.END)
    output.insert(tk.END, "ID | Lietotājvārds\n")

    for user in get_users():
        output.insert(tk.END, str(user) + "\n")


def showReviews():
    output.delete("1.0", tk.END)
    output.insert(
        tk.END,
        "Filma | Lietotājs | Vērtējums | Atsauksme\n"
    )

    for review in get_reviews():
        output.insert(tk.END, str(review) + "\n")


# Veidojam logu.
window = tk.Tk()
window.title("Kino datubāze — beta")
window.geometry("850x720")

header = tk.Label(
    window,
    text="Kino datubāze",
    font=("Arial", 20, "bold")
)
header.pack(pady=10)

# Veidojam cilnes.
tabs = ttk.Notebook(window)
tabs.pack(fill="both", expand=True, padx=20)

movie_tab = ttk.Frame(tabs)
user_tab = ttk.Frame(tabs)
review_tab = ttk.Frame(tabs)

tabs.add(movie_tab, text="Filmas")
tabs.add(user_tab, text="Lietotāji")
tabs.add(review_tab, text="Vērtējumi un atsauksmes")

# Filmu bloks.
movie_block = tk.LabelFrame(
    movie_tab,
    text="Pievienot vai meklēt filmu",
    padx=10,
    pady=10
)
movie_block.pack(fill="x", padx=20, pady=10)

tk.Label(movie_block, text="Filmas nosaukums").pack()

movie_input = tk.Entry(movie_block, width=60)
movie_input.pack(pady=5)

tk.Button(
    movie_block,
    text="Pievienot filmu",
    command=addFromWindow
).pack(pady=5)

tk.Button(
    movie_block,
    text="Rādīt / meklēt filmas",
    command=showMovies
).pack(pady=5)

# Lietotāju bloks.
user_block = tk.LabelFrame(
    user_tab,
    text="Pievienot lietotāju",
    padx=10,
    pady=10
)
user_block.pack(fill="x", padx=20, pady=10)

tk.Label(user_block, text="Lietotājvārds").pack()

user_input = tk.Entry(user_block, width=60)
user_input.pack(pady=5)

tk.Button(
    user_block,
    text="Pievienot lietotāju",
    command=addFromWindow2
).pack(pady=5)

tk.Button(
    user_block,
    text="Rādīt lietotājus",
    command=showUsers
).pack(pady=5)

# Atsauksmju bloks.
review_block = tk.LabelFrame(
    review_tab,
    text="Pievienot vai labot atsauksmi",
    padx=10,
    pady=10
)
review_block.pack(fill="x", padx=20, pady=10)

tk.Label(review_block, text="Filmas ID").pack()

movie_id_input = tk.Entry(review_block, width=60)
movie_id_input.pack(pady=5)

tk.Label(review_block, text="Lietotāja ID").pack()

user_id_input = tk.Entry(review_block, width=60)
user_id_input.pack(pady=5)

tk.Label(review_block, text="Vērtējums (1–10)").pack()

rating_input = tk.Entry(review_block, width=60)
rating_input.pack(pady=5)

tk.Label(review_block, text="Atsauksme").pack()

review_input = tk.Entry(review_block, width=60)
review_input.pack(pady=5)

tk.Button(
    review_block,
    text="Saglabāt",
    command=addFromWindow3
).pack(pady=5)

tk.Button(
    review_block,
    text="Rādīt atsauksmes",
    command=showReviews
).pack(pady=5)

# Paziņojumi.
result = tk.Label(window, text="", fg="green")
result.pack(pady=5)

# Sarakstu parādīšana.
output = tk.Text(window, width=100, height=10)
output.pack(padx=20, pady=10)

showMovies()
window.mainloop()