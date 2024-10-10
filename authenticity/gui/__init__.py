"""
__init__.py
Author:     Marcus T Taylor
Created:    03.11.23
Modified:   15.03.24
"""
from tkinter import *

import customtkinter


def main() -> None:
    app = customtkinter.CTk()
    app.title("Authenticity")
    main_frame = customtkinter.CTkFrame(app)
    main_frame.pack()
    test_button = customtkinter.CTkButton(main_frame, text="Authenticity")
    test_button.grid(column=0, row=0)
    app.mainloop()
