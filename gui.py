import tkinter as tk
from tkinter import ttk
from ttkbootstrap import Style
from card_handler import save_set, save_card
from review_logic import start_review, flip_card, mark_card


def create_gui(data):
    root = tk.Tk()
    Style('superhero')
    root.title('Flashcards')
    root.geometry('400x400')
    root.resizable(False, False)

    notebook = ttk.Notebook(root)
    notebook.pack(expand=True, fill='both', padx=10, pady=5)

    set_frame = tk.Frame(notebook)
    card_frame = tk.Frame(notebook)
    review_frame = tk.Frame(notebook)

    notebook.add(set_frame, text='Set')
    notebook.add(card_frame, text='Card')
    notebook.add(review_frame, text='Review')

    # Set Frame
    set_name_var = tk.StringVar()
    ttk.Label(set_frame, text='Set Name').pack(pady=8)
    set_name_entry = ttk.Entry(set_frame, textvariable=set_name_var)
    set_name_entry.pack(pady=8)
    ttk.Button(set_frame, text='Create Set', command=lambda: save_set(
        set_name_var, data, options=[card_set_combo, review_set_combo])).pack(pady=8)

    # Card Frame
    card_set_var = tk.StringVar()
    ttk.Label(card_frame, text='Select Set').pack(pady=8)
    card_set_combo = ttk.Combobox(card_frame, textvariable=card_set_var)
    card_set_combo['values'] = list(data['sets'].keys())
    card_set_combo.pack(pady=8)

    word_var = tk.StringVar()
    definition_var = tk.StringVar()
    ttk.Label(card_frame, text='Word').pack(pady=8)
    ttk.Entry(card_frame, textvariable=word_var).pack(pady=8)
    ttk.Label(card_frame, text='Definition').pack(pady=8)
    ttk.Entry(card_frame, textvariable=definition_var).pack(pady=8)
    ttk.Button(card_frame, text='Save Card', command=lambda: save_card(
        word_var, definition_var, data, card_set_var.get(), card_set_combo)).pack(pady=8)

    # Review Frame
    review_set_var = tk.StringVar()
    state = {'cards': [], 'index': 0, 'flipped': False}

    select_set_label = ttk.Label(review_frame, text='Select Set')
    select_set_label.pack(pady=8)
    review_set_combo = ttk.Combobox(review_frame, textvariable=review_set_var)
    review_set_combo['values'] = list(data['sets'].keys())
    review_set_combo.pack(pady=8)

    start_button = ttk.Button(
        review_frame,
        text="Start Review",
        command=lambda: start_review(
            review_set_var, data, state, review_frame, start_button, word_label, definition_label, progress_label, flip_button, correct_button, wrong_button, review_set_combo, select_set_label
        )
    )
    start_button.pack(pady=8)

    progress_label = ttk.Label(review_frame, text="Progress: 0%")
    word_label = ttk.Label(review_frame, text="Word: ???")
    definition_label = ttk.Label(review_frame, text="Definition: ???")

    flip_button = ttk.Button(review_frame, text="Flip", state='disabled', command=lambda: flip_card(
        state, word_label, definition_label, flip_button, correct_button, wrong_button))

    correct_button = ttk.Button(review_frame, text='Correct', state='disabled', command=lambda: mark_card(
        state, data, True, review_set_var.get(), progress_label, word_label, definition_label, flip_button, correct_button, wrong_button))

    wrong_button = ttk.Button(review_frame, text='Wrong', state='disabled', command=lambda: mark_card(
        state, data, False, review_set_var.get(), progress_label, word_label, definition_label, flip_button, correct_button, wrong_button))

    root.mainloop()
