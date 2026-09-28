import tkinter as tk 
import random

# -----------------------------
# GAME DATA
# -----------------------------

words = [
    "python",
    "computer",
    "program",
    "coding",
    "school"
]

word = random.choice(words)
guessed_letters = set()
wrong_guesses = 0
max_wrong = 6


# -----------------------------
# CREATE MAIN WINDOW
# -----------------------------

window = tk.Tk()
window.title("Hangman Game")
window.geometry("700x650")
window.resizable(False, False)


# -----------------------------
# TITLE
# -----------------------------

title = tk.Label(
    window,
    text="HANGMAN GAME",
    font=("Arial", 28, "bold")
)

title.pack(pady=15)


# -----------------------------
# CANVAS FOR HANGMAN
# -----------------------------

canvas = tk.Canvas(
    window,
    width=300,
    height=250,
    bg="white"
)

canvas.pack()


# -----------------------------
# WORD DISPLAY
# -----------------------------

word_label = tk.Label(
    window,
    text="",
    font=("Arial", 26, "bold")
)

word_label.pack(pady=15)


# -----------------------------
# WRONG GUESS DISPLAY
# -----------------------------

lives_label = tk.Label(
    window,
    text="Wrong guesses: 0 / 6",
    font=("Arial", 14)
)

lives_label.pack()


# -----------------------------
# UPDATE WORD
# -----------------------------

def update_word():
    display = ""

    for letter in word:
        if letter in guessed_letters:
            display += letter.upper() + " "
        else:
            display += "_ "

    word_label.config(text=display)


# -----------------------------
# DRAW HANGMAN
# -----------------------------

def draw_hangman():

    if wrong_guesses == 1:
        # Base
        canvas.create_line(50, 230, 250, 230, width=5)

    elif wrong_guesses == 2:
        # Vertical pole
        canvas.create_line(100, 230, 100, 40, width=5)

    elif wrong_guesses == 3:
        # Top horizontal pole
        canvas.create_line(100, 40, 210, 40, width=5)

    elif wrong_guesses == 4:
        # Rope
        canvas.create_line(210, 40, 210, 75, width=4)

        # Head
        canvas.create_oval(
            180, 75, 240, 135,
            width=4
        )

    elif wrong_guesses == 5:
        # Body
        canvas.create_line(
            210, 135, 210, 195,
            width=4
        )

        # Arms
        canvas.create_line(
            210, 150, 175, 175,
            width=4
        )

        canvas.create_line(
            210, 150, 245, 175,
            width=4
        )

    elif wrong_guesses == 6:
        # Legs
        canvas.create_line(
            210, 195, 180, 225,
            width=4
        )

        canvas.create_line(
            210, 195, 240, 225,
            width=4
        )


# -----------------------------
# CHECK WIN
# -----------------------------

def check_win():

    for letter in word:
        if letter not in guessed_letters:
            return False

    return True


# -----------------------------
# LETTER BUTTON FUNCTION
# -----------------------------

def guess_letter(letter):

    global wrong_guesses

    # Ignore if game already finished
    if wrong_guesses >= max_wrong:
        return

    # Ignore already guessed letter
    if letter in guessed_letters:
        return

    # Save guessed letter
    guessed_letters.add(letter)

    # Disable button
    buttons[letter].config(state="disabled")

    # Correct guess
    if letter in word:
        update_word()

        if check_win():
            result_label.config(
                text="🎉 YOU WIN!",
                font=("Arial", 20, "bold")
            )

            disable_all_buttons()

    # Wrong guess
    else:
        wrong_guesses += 1

        lives_label.config(
            text=f"Wrong guesses: {wrong_guesses} / 6"
        )

        draw_hangman()

        if wrong_guesses == max_wrong:
            result_label.config(
                text=f"GAME OVER! Word was: {word.upper()}",
                font=("Arial", 18, "bold")
            )

            disable_all_buttons()


# -----------------------------
# CREATE LETTER BUTTONS
# -----------------------------

button_frame = tk.Frame(window)
button_frame.pack(pady=15)

buttons = {}

alphabet = "abcdefghijklmnopqrstuvwxyz"

for i, letter in enumerate(alphabet):

    button = tk.Button(
        button_frame,
        text=letter.upper(),
        width=4,
        height=2,
        font=("Arial", 10, "bold"),
        command=lambda l=letter: guess_letter(l)
    )

    button.grid(
        row=i // 9,
        column=i % 9,
        padx=3,
        pady=3
    )

    buttons[letter] = button


# -----------------------------
# RESULT MESSAGE
# -----------------------------

result_label = tk.Label(
    window,
    text="Guess a letter!",
    font=("Arial", 16)
)

result_label.pack(pady=5)


# -----------------------------
# DISABLE ALL BUTTONS
# -----------------------------

def disable_all_buttons():

    for button in buttons.values():
        button.config(state="disabled")


# -----------------------------
# RESTART GAME
# -----------------------------

def restart_game():

    global word
    global guessed_letters
    global wrong_guesses

    word = random.choice(words)

    guessed_letters = set()

    wrong_guesses = 0

    canvas.delete("all")

    lives_label.config(
        text="Wrong guesses: 0 / 6"
    )

    result_label.config(
        text="Guess a letter!"
    )

    for button in buttons.values():
        button.config(state="normal")

    update_word()


# -----------------------------
# PLAY AGAIN BUTTON
# -----------------------------

restart_button = tk.Button(
    window,
    text="PLAY AGAIN",
    font=("Arial", 14, "bold"),
    command=restart_game
)

restart_button.pack(pady=10)


# -----------------------------
# START GAME
# -----------------------------

update_word()

window.mainloop()