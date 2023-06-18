from tkinter import *       # Importing tkinter module.
import pandas as pd         # To efficiently read the CSV file.
import random               # To perform random operations.

# ------------------------------------------------ CONSTANTS ----------------------------------------------------------------

BACKGROUND_COLOR = "#B1DDC6"

# ------------------------------------------------ BACKEND ----------------------------------------------------------------

try:
    data = pd.read_csv('data/words_to_learn.csv', encoding = 'utf-8')       # This is a dataframe. If words_to_learn.csv is not avaialble then except block gets triggered. 
except FileNotFoundError:
    data = pd.read_csv('data/hi_to_en_words.csv', encoding = 'utf-8')       # This is also a dataframe. If words_to_learn.csv is not avaialble then this block of code gets triggered.
    
data_dict_list = data.to_dict(orient = "records")      # Converting the dataframe to a dictionary. A list of dictionary is being returned using orient = "records" as a paramter.
# orient = "records" helps us to orient the dictionary in the form of column_name and row_value.

current_card = {}       # global dictionary named current_card to access this dictionary by the below functions.

def next_card():
    global current_card, flip_timer
    window.after_cancel(flip_timer)     # If the button is pressed continuously then it clear the previous timer. 
    
    current_card = random.choice(data_dict_list)        # Getting random word from the dictionary list.
    canvas.itemconfig(card_layout, image=card_front_image)
    canvas.itemconfig(card_title, text = "Hindi", fill = "#000000")
    canvas.itemconfig(card_word, text = current_card["Hindi Words"], fill = "#000000")
    
    flip_timer = window.after(4000, func = flip_card)    # After 4000 ms or 4 seconds call the function flip_card.
    
def flip_card():
    canvas.itemconfig(card_layout, image=card_back_image)
    canvas.itemconfig(card_title, text = "English", fill = "#ffffff")
    canvas.itemconfig(card_word, text = current_card["English Words"].title(), fill = "#ffffff")
    
def is_known():
    data_dict_list.remove(current_card)     # Removing the known words from the dictionary.
    # print(len(data_dict_list))            # Checking whether the words are removed or not by using the length function.
    data = pd.DataFrame(data_dict_list)
    data.to_csv("data/words_to_learn.csv", index=False)
    next_card()                             # Calling the next card.
    
# ------------------------------------------------ UI SETUP -----------------------------------------------------------------

window = Tk()                           # Creating window by creating object of the class Tk which is available inside the tkinter module.
window.title("Flash Card Application - Made By Koushik Sadhu")  # Setting the title name.
window.config(padx = 50, pady = 50, bg = BACKGROUND_COLOR)     # Providing 50px padding on x and y axis of the window and setting up the background color using bg parameter.

flip_timer =  window.after(4000, func = flip_card)    # After 4000 ms or 4 seconds call the function flip_card

canvas = Canvas(width = 800, height = 526)     # Creating a canvas of the given width and height.

app_name = Label(text = "FLASHY",  font = ("Courier", 40, "bold"), bg = BACKGROUND_COLOR, fg = "WHITE", pady = 20)
app_name.grid(row = 0, column = 0, columnspan = 2)

card_front_image = PhotoImage(file="images/card_front.png")
card_back_image = PhotoImage(file="images/card_back.png")

card_layout = canvas.create_image(400, 263, image=card_front_image)
canvas.config(bg = BACKGROUND_COLOR, highlightthickness = 0)        # To remove the corner edges white color to the Background color and remove the border thickness.

card_title = canvas.create_text(400, 150, text = "", font = ("Times New Roman", 25, "normal"))       # Creating text at the given x and y axis with the provided Text and FONT.
card_word = canvas.create_text(400, 263, text = "", font = ("Times New Roman", 40, "bold"))       # Creating text at the given x and y axis with the provided Text and FONT.

canvas.grid(row = 1, column = 0, columnspan = 2)

cross_image = PhotoImage(file="images/wrong.png")               # Opening the image using PhotoImage class
no_button = Button(image=cross_image, highlightthickness = 0, command = next_card)   # Applying the image in the button with the given properties.
no_button.grid(row = 2, column = 0)                             # Setting up the button position using grid.

tick_image = PhotoImage(file="images/right.png")                # Opening the image using PhotoImage class
yes_button = Button(image=tick_image, highlightthickness = 0, command = is_known)   # Applying the image in the button with the given properties.
yes_button.grid(row = 2, column = 1)                            # Setting up the button position using grid.

next_card()     # Calling the next_card function for the first time.

window.mainloop()