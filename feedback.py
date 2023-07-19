from tkinter import *
import tkinter as tk
from tkinter import messagebox
from tkinter import scrolledtext
from pymongo import MongoClient
import customtkinter
from datetime import *
import time
import re
import pymongo


client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["feedback"]
collection = db["reviews"]

customtkinter.set_appearance_mode("Dark")
customtkinter.set_default_color_theme("green")

root = customtkinter.CTk()
root.title("Feedback")
root.geometry("390x620")
root.iconbitmap("fform.ico")


view_frame = None
delete_frame = None
submit_frame = None
login_frame = None
username_entry = None
password_entry = None


def show_menu():
    if view_frame:
        view_frame.destroy()
    if delete_frame:
        delete_frame.destroy()
    if login_frame:
        login_frame.destroy()

    menu_frame = customtkinter.CTkFrame(root, width=250, height=180)
    menu_frame.place(x=10, y=10)

    view_button = customtkinter.CTkButton(menu_frame, text="View Feedback", width=15, command=show_view_frame)
    view_button.place(x=75, y=20)

    delete_button = customtkinter.CTkButton(menu_frame, text="Delete Feedback", width=15, command=show_delete_frame)
    delete_button.place(x=70, y=60)

    def go_back():
        menu_frame.destroy()

    back_button = customtkinter.CTkButton(menu_frame, text="Logout", command=go_back)
    back_button.place(x=60, y=110)


def show_view_frame():
    if delete_frame:
        delete_frame.destroy()
    if login_frame:
        login_frame.destroy()

    initialize_view_frame()


def show_delete_frame():
    if view_frame:
        view_frame.destroy()
    if login_frame:
        login_frame.destroy()

    initialize_delete_frame()


def initialize_view_frame():
    global view_frame

    if view_frame:
        view_frame.destroy()

    view_frame = customtkinter.CTkFrame(root, width=400, height=640)
    view_frame.place(x=0, y=0)


    feedback_listbox = Listbox(view_frame, font="arial 16", width=39, height=25)
    feedback_listbox.place(x=8, y=30)


    reviews = collection.find()


    for entry in reviews:
        name = entry.get('name', 'N/A')
        email = entry.get('email', 'N/A')
        feedback = entry.get('feedback', 'N/A')
        rating = entry.get('rating', 'N/A')
        feedback_listbox.insert(END, f"Name: {name}\n Email: {email}\n Feedback: {feedback}\n Rating: {rating}\n")

    back_button = customtkinter.CTkButton(view_frame, text="Back", command=show_menu)
    back_button.place(x=120, y=560)


def initialize_delete_frame():
    global delete_frame

    if delete_frame:
        delete_frame.destroy()

    delete_frame = customtkinter.CTkFrame(root, width=400, height=640)
    delete_frame.place(x=0, y=0)


    feedback_listbox = Listbox(delete_frame, font="arial 16", width=39, height=25)
    feedback_listbox.place(x=8, y=30)


    reviews = collection.find()


    for index, entry in enumerate(reviews):
        name = entry.get('name', 'N/A')
        email = entry.get('email', 'N/A')
        feedback = entry.get('feedback', 'N/A')
        rating = entry.get('rating', 'N/A')
        feedback_listbox.insert(END, f"Index: {index}\nName: {name}\nEmail: {email}\nFeedback: {feedback}\nRating: {rating}\n")

    def confirm_delete():
        response = messagebox.askyesno("Confirmation", "Are you sure you want to delete?")
        if response:
            selected_index = feedback_listbox.curselection()

            if len(selected_index) > 0:

                index = int(selected_index[0])


                entry = collection.find()[index]


                collection.delete_one({'_id': entry['_id']})


                feedback_listbox.delete(0, END)


                reviews = collection.find()
                for idx, e in enumerate(reviews):
                    name = e.get('name', 'N/A')
                    email = e.get('email', 'N/A')
                    feedback = e.get('feedback', 'N/A')
                    rating = e.get('rating', 'N/A')
                    feedback_listbox.insert(END, f"Index: {idx}\nName: {name}\nEmail: {email}\nFeedback: {feedback}\nRating: {rating}\n")
                messagebox.showinfo("Deleted", "Feedback deleted")

    delete_button = customtkinter.CTkButton(delete_frame, text="Delete", command=confirm_delete)
    delete_button.place(x=120, y=550)

    back_button = customtkinter.CTkButton(delete_frame, text="Back", width=10, command=show_menu)
    back_button.place(x=173, y=585)


def view_feedbacks():
    feedbacks = collection.find({})
    feedback_list.delete(0, tk.END)
    for feedback in feedbacks:
        feedback_id = feedback['_id']
        name = feedback.get('name', 'N/A')
        comment = feedback.get('comment', 'N/A')
        feedback_list.insert(tk.END, f"ID: {feedback_id}, Name: {name}, Comment: {comment}")


def delete_feedback():
    selected_feedback = feedback_list.curselection()
    if selected_feedback:
        feedback_id = feedback_list.get(selected_feedback)[4:24]
        collection.delete_one({"_id": pymongo.ObjectId(feedback_id)})
        messagebox.showinfo("Success", "Feedback deleted successfully!")
    else:
        messagebox.showerror("Error", "Please select a feedback to delete.")


def admin_login():
    global username_entry
    global password_entry

    username = username_entry.get()
    password = password_entry.get()

    admin = collection.find_one({"username": username, "password": password, "role": "admin"})
    if admin is not None:
        messagebox.showinfo("sucess", "Admin login successful!")
        show_menu()
    else:
        messagebox.showerror("Error", "Invalid admin credentials. Login failed.")


def admin_frame():
    global login_frame

    if login_frame:
        login_frame.destroy()

    global username_entry
    global password_entry

    login_frame = customtkinter.CTkFrame(root, width=200, height=220)
    login_frame.place(x=10, y=10)

    username_label = customtkinter.CTkLabel(login_frame, text="Username:")
    username_label.place(x=20, y=10)
    username_entry = customtkinter.CTkEntry(login_frame)
    username_entry.place(x=20, y=40)

    password_label = customtkinter.CTkLabel(login_frame, text="Password:")
    password_label.place(x=20, y=70)
    password_entry = customtkinter.CTkEntry(login_frame, show="*")
    password_entry.place(x=20, y=100)

    login_button = customtkinter.CTkButton(login_frame, text="Login", command=admin_login)
    login_button.place(x=20, y=140)

    def go_back():
        login_frame.destroy()

    back_button = customtkinter.CTkButton(login_frame, text="Back", width=20, command=go_back)
    back_button.place(x=70, y=180)


admin_button = customtkinter.CTkButton(root, text="Admin login", command=admin_frame)
admin_button.place(x=10, y=10)

def validate_name(name):
    pattern = r'^[A-Za-z]+$'
    return re.match(pattern, name) is not None

def validate_email(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email) is not None

def validate_feedback(feedback):
    max_length = 500
    return len(feedback) <= max_length

def submit_feedback():
    name = n_entry.get()
    email = e_entry.get()
    feedback = tk_textbox.get("1.0", "end-1c")
    rating = radio_var.get()

    if name and email and feedback and rating:

        if not validate_name(name):
            messagebox.showerror("Error", "Invalid name format.")
            return

        if not validate_email(email):
            messagebox.showerror("Error", "Invalid email format.")
            return

        if not validate_feedback(feedback):
            messagebox.showerror("Error", "Feedback exceeds the maximum length limit.")
            return

        entry = {
            'name': name,
            'email': email,
            'feedback': feedback,
            'rating': rating
        }


        collection.insert_one(entry)


        n_entry.delete(0, END)
        e_entry.delete(0, END)
        tk_textbox.delete("1.0", END)


        messagebox.showinfo("Success", "Feedback submitted successfully!")

    else:
        messagebox.showerror("Error", "Please fill in all fields.")


radio_var = IntVar()
def radiobutton_event():
    print("radiobutton toggled, current value:", radio_var.get())

radiobutton_1 = customtkinter.CTkRadioButton(root, text="1 star",
                                             command=radiobutton_event, variable=radio_var, value=1)
radiobutton_2 = customtkinter.CTkRadioButton(root, text="2 star",
                                             command=radiobutton_event, variable=radio_var, value=2)
radiobutton_3 = customtkinter.CTkRadioButton(root, text="3 star",
                                             command=radiobutton_event, variable=radio_var, value=3)
radiobutton_4 = customtkinter.CTkRadioButton(root, text="4 star",
                                             command=radiobutton_event, variable=radio_var, value=4)
radiobutton_5 = customtkinter.CTkRadioButton(root, text="5 star",
                                             command=radiobutton_event, variable=radio_var, value=5)

radiobutton_1.place(x=20, y=470)
radiobutton_2.place(x=95, y=470)
radiobutton_3.place(x=170, y=470)
radiobutton_4.place(x=245, y=470)
radiobutton_5.place(x=320, y=470)


def combobox_callback(choice):
    if choice == "Light theme":
        customtkinter.set_appearance_mode("light")
    elif choice == "Dark theme":
        customtkinter.set_appearance_mode("dark")


combobox = customtkinter.CTkComboBox(root, values=["Light theme", "Dark theme"], command=combobox_callback)
combobox.place(x=220, y=10)
combobox.set("Dark theme")

n_entry = customtkinter.CTkEntry(root)
n_entry.place(x=90, y=101)

n_label = customtkinter.CTkLabel(root, text="Name")
n_label.place(x=20, y=100)

e_entry = customtkinter.CTkEntry(root)
e_entry.place(x=90, y=151)

e_label = customtkinter.CTkLabel(root, text="Email")
e_label.place(x=20, y=150)

tk_textbox = customtkinter.CTkTextbox(root)
tk_textbox.place(x=100, y=200)

ctk_textbox_scrollbar = customtkinter.CTkScrollbar(root, command=tk_textbox.yview)
ctk_textbox_scrollbar.place(x=290, y=200)
tk_textbox.configure(yscrollcommand=ctk_textbox_scrollbar.set)

f_label = customtkinter.CTkLabel(root, text="Feedback")
f_label.place(x=20, y=200)

r_label = customtkinter.CTkLabel(root, text="Rating")
r_label.place(x=20, y=430)

submit_button = customtkinter.CTkButton(root, text="Submit", command=submit_feedback)
submit_button.place(x=115, y=550)


def confirm_quit():
    response = messagebox.askyesno("Confirmation", "Are you sure you want to quit?")
    if response:
        root.destroy()


root.protocol("WM_DELETE_WINDOW", confirm_quit)

root.mainloop()
