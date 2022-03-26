from tkinter import *
import pandas
import random
import csv

BACKGROUND_COLOR = "#B1DDC6"

try:
    words_to_learn = pandas.read_csv("data/words_to_learn.csv", encoding="windows-1252")
except FileNotFoundError:
    original_data = pandas.read_csv("data/french_words.csv")
    eng = original_data["English"].to_list()
    french = original_data["French"].to_list()
    words_dictionary = {french[_]: eng[_] for _ in range(len(eng))}
else:
    eng = words_to_learn["English"].to_list()
    french = words_to_learn["French"].to_list()
    words_dictionary = {french[_]: eng[_] for _ in range(len(eng))}


def next_word():
    global random_word
    random_word = random.choice(list(words_dictionary))
    canvas.itemconfig(card_image, image=french_img)
    canvas.itemconfig(card_title, text="French")
    canvas.itemconfig(card_word, text=random_word)
    window.after(3000, english)
    window.after_cancel(english)


def english():
    canvas.itemconfig(card_image, image=eng_img)
    canvas.itemconfig(card_title, text="English")
    canvas.itemconfig(card_word, text=words_dictionary[random_word])


def word_known():
    french.remove(random_word)
    eng.remove(words_dictionary[random_word])
    words_dictionary.pop(random_word)
    with open('data/words_to_learn.csv', 'w', newline='') as unknown_words:
        header_key = ["French", "English"]
        new = csv.DictWriter(unknown_words, fieldnames=header_key)
        new.writeheader()
        for french_word in words_dictionary:
            new.writerow({'French': french_word, 'English': words_dictionary[french_word]})
    next_word()


window = Tk()
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)
window.title("French Flashcards")

canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
french_img = PhotoImage(file="images/card_front.png")
eng_img = PhotoImage(file="images/card_back.png")
card_image = canvas.create_image(400, 263, image=french_img)
card_title = canvas.create_text(400, 150, text="", fill="black", font=('ariel', 40, 'italic'))
card_word = canvas.create_text(400, 263, text="", fill="black", font=('ariel', 60, 'bold'))
canvas.grid(column=0, row=0, columnspan=2)

yes_image = PhotoImage(file="images/right.png")
yes_button = Button(image=yes_image, highlightthickness=0, command=word_known)
yes_button.grid(column=1, row=1)

no_image = PhotoImage(file="images/wrong.png")
no_button = Button(image=no_image, highlightthickness=0, command=next_word)
no_button.grid(column=0, row=1)

next_word()

window.mainloop()
