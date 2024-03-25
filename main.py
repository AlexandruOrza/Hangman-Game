import csv
from random import choice
import requests


def draw_word():
    drawn_word = draw_word_api()
    if drawn_word is None:
        drawn_word = draw_word_csv()
    return drawn_word


# Returns a word in string format from API
def draw_word_api():
    try:
        response = requests.get('https://random-word-api.herokuapp.com/word',
                                allow_redirects=False, timeout=5)
        status_code = response.status_code
        drawn_word_api = ""
        if status_code == 200:
            drawn_word_api = response.json()
            drawn_word_api = "".join(drawn_word_api)
        return drawn_word_api
    except requests.exceptions.ConnectionError:
        return None
    except requests.exceptions.Timeout:
        return None


# Returns a word in string format from .csv file
def draw_word_csv():
    with open("wordlist.csv", encoding="utf-8", newline="") as csvfile:
        reader = csv.reader(csvfile)
        drawn_word_csv = choice(list(reader))
        drawn_word_csv = "".join(drawn_word_csv)
        return drawn_word_csv


# Hangman State
hangman_steps = [
    """
------
|  |
|  O
| /|\\
| / \\
|
|
|___
    """,
    """
------
|  |
|  O
| /|\\
| /
|
|
|___
    """,
    """
------
|  |
|  O
| /|\\
|
|
|
|___
    """,
    """
------
|  |
|  O
| /|
|
|
|
|___
    """,
    """
------
|  |
|  O
|  |
|
|
|
|___
    """,
    """
------
|  |
|  O
|
|
|
|
|___
    """,
    """
------
|  |
|
|
|
|
|
|___
    """
                 ]


# Takes the player input and checks if it is only one letter
def player_input():
    while True:
        letter_input = input("Enter a letter: ").lower()
        if letter_input.isalpha() and len(letter_input) == 1:
            return letter_input
        print("Please insert only a letter!")


# Checks if the inputted letter is in the drawn_word
# and updates the display_word
def check_letter(user_letter, drawn_word, display_word):
    correct_guess = False
    for i in range(len(drawn_word)):
        if user_letter == drawn_word[i]:
            display_word[i] = user_letter
            correct_guess = True
    return correct_guess, display_word


# Updates user about their guess and attempts
def is_correct_guess(attempts, correct_guess):
    if correct_guess:
        print("Correct guess!")
    else:
        attempts -= 1
        print(f"You guessed wrong! Attempts left: {attempts}")
    return attempts


# Main function of the game
def game_setup():
    drawn_word = list(draw_word())
    display_word = list("_" * len(drawn_word))
    attempts = 6

    while display_word != drawn_word:
        print(*hangman_steps[attempts], sep="")
        print(*display_word, sep="")
        user_letter = player_input()
        correct_guess, display_word = check_letter(
            user_letter, drawn_word, display_word)
        attempts = is_correct_guess(attempts, correct_guess)
# Win/Lose conditions
        if attempts == 0:
            print(hangman_steps[attempts], sep="")
            print(*display_word, sep="")
            correct_word = "".join(drawn_word)
            print(f"You lost!\nThe word was {correct_word}")
            break
        if display_word == drawn_word:
            print(*hangman_steps[attempts], sep="")
            print(*display_word, sep="")
            print("You won!")
    print("GAME OVER")


# New game loop
def new_game():
    print("Welcome to Hangman!")
    replay = True
    while replay:
        game_setup()
        while True:
            print("Do you want to play again?\nY/N?")
            user_choice = str(input()).lower()
            if user_choice == "y":
                replay = True
                break
            if user_choice == "n":
                replay = False
                break


new_game()
