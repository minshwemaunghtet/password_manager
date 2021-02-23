from tkinter import *
from tkinter import messagebox
from random import choice, randint, shuffle
import pyperclip
import json


# Password Generator Mechanism
def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']


    # Generate by using list comprehension
    password_letters = [choice(letters) for _ in range(randint(6, 8))]
    password_symbols = [choice(symbols) for _ in range(randint(3, 6))]
    password_numbers = [choice(numbers) for _ in range(randint(3, 6))]

    password_list = password_letters + password_symbols + password_numbers
    shuffle(password_list)

    final_password = "".join(password_list)  # It joins characters in the list and returns like a string
    password_entry.insert(0, final_password)  # It appears on Password entry when user hits the button
    pyperclip.copy(final_password)  # Using pyperclip will get the string and copy to the clipboard


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save_info():
    # Get the user info from three entries which was entered in the entries box
    website = website_entry.get()
    email = email_entry.get()
    password = password_entry.get()

    new_data = {     # It creates json data format which is similar like dictionarie
        website : {
            "email": email,
            "password": password,
        }
    }

    # Check whether user left the entires empty or not
    # It will check only webiste and password entries since email is u
    if len(website) == 0 or len(password) == 0:
        messagebox.showinfo(title="Oops", message="Please make sure you haven't left any fields empty!")
    else:
        try:
            with open("user_data.json", "r") as data_file:
                data = json.load(data_file)  # Reading old json data

        except FileNotFoundError:
            with open("user_data.json", "w") as data_file:
                json.dump(new_data, data_file, indent=4)

        else:   # If everything in try block is successful
            data.update(new_data)  # Updating old data with new data

            with open("user_data.json", "w") as data_file:
                json.dump(data, data_file, indent=4)  # Saving updated data

        finally:  # No matter if everything in the block above is succeed or fail
            website_entry.delete(0, END)  # It will clear the field from start to end position for next input
            password_entry.delete(0, END)  # It will clear the field from start to end position for next input



# ---------------------------- FIND PASSWORD ------------------------------- #
def find_password():
    website = website_entry.get()
    try:
        with open("user_data.json") as data_file:
            data = json.load(data_file)
    except FileNotFoundError:  # Potential issue as soon as user opens
        messagebox.showinfo(title="Error", message="No Saved Data File Found")
    else:  # If condition in try block triggered
        if website in data:
            email = data[website]["email"]
            password = data[website]["password"]
            messagebox.showinfo(title=website, message=f"Email: {email}\nPassword: {password}")
        else:
            messagebox.showinfo(title="Error", message=f"There is no data for {website}")




# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

canvas = Canvas(height=200, width=200)
logo_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_img)
canvas.grid(row=0, column=1)

#Labels
website_label = Label(text="Website:")
website_label.grid(row=1, column=0)
email_label = Label(text="Email/Username:")
email_label.grid(row=2, column=0)
password_label = Label(text="Password:")
password_label.grid(row=3, column=0)

#Entries
website_entry = Entry(width=21)
website_entry.grid(row=1, column=1)
website_entry.focus()
email_entry = Entry(width=39)
email_entry.grid(row=2, column=1, columnspan=2)
email_entry.insert(0, "minshwemaunghtet@gmail.com")
password_entry = Entry(width=21)
password_entry.grid(row=3, column=1)

# Buttons
search_button = Button(text="Search", width=13, command=find_password)
search_button.grid(row=1, column=2)
generate_password_button = Button(text="Generate Password", command=generate_password)
generate_password_button.grid(row=3, column=2)
add_button = Button(text="Add", width=36, command=save_info)
add_button.grid(row=4, column=1, columnspan=2)

window.mainloop()
