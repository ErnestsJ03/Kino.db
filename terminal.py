import sqlite3

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


while True:
    print("\nKINO DATUBĀZE")
    print("1 - pievienot filmu")
    print("2 - pievienot lietotāju")
    print("3 - pievienot vai labot vērtējumu un atsauksmi")
    print("4 - parādīt filmas")
    print("5 - parādīt lietotājus")
    print("6 - parādīt atsauksmes")
    print("7 - meklēt filmu")
    print("0 - iziet")

    choise = input("Izvēle: ")

    try:
        if choise == "1":
            name = input("Filmas nosaukums: ")
            movie_id = add_movie(name)

            print("Filma pievienota. ID:", movie_id)

        elif choise == "2":
            name = input("Lietotājvārds: ")
            user_id = add_user(name)

            print("Lietotājs pievienots. ID:", user_id)

        elif choise == "3":
            print("\nFilmas:")

            for movie in get_movies():
                print(movie)

            print("\nLietotāji:")

            for user in get_users():
                print(user)

            movie_id = input("Filmas ID: ")
            user_id = input("Lietotāja ID: ")
            rating = input("Vērtējums (1–10): ")
            review = input("Atsauksme: ")

            add_review(movie_id, user_id, rating, review)

            print("Saglabāts.")

        elif choise == "4":
            for movie in get_movies():
                print(movie)

        elif choise == "5":
            for user in get_users():
                print(user)

        elif choise == "6":
            for review in get_reviews():
                print(review)

        elif choise == "7":
            name = input("Filmas nosaukums vai tā daļa: ")

            for movie in get_movies(name):
                print(movie)

        elif choise == "0":
            break

        else:
            print("Nezināma izvēle.")

    except ValueError as error:
        print("Kļūda:", error)

    except sqlite3.IntegrityError:
        print("Dublikāts vai nepareizs filmas/lietotāja ID.")