import json
import pathlib
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from ttkbootstrap import Style

def save_set(entry, data, **kwargs):
    set_name = entry.get()
    if set_name:
        data['sets'][set_name] = []
        with open('data.json', 'w') as file:
            json.dump(data, file)
        messagebox.showinfo('Success', f'Set {set_name} saved successfully')
    else:
        messagebox.showerror('Error', 'Set name cannot be empty')
    entry.set('')
    if 'options' in kwargs:
        options = kwargs['options']
        for o in options:
            o['values'] = list(data['sets'].keys())


def save_card(word, definition, data, set_name):
    card_word = word.get()
    card_definition = definition.get()
    if card_word and card_definition:
        try:
            data['sets'][set_name].append({'word': card_word, 'definition': card_definition})
            with open('data.json', 'w') as file:
                json.dump(data, file)
            messagebox.showinfo('Success', 'Card saved successfully')
            word.set('')
            definition.set('')
        except KeyError:
            messagebox.showerror('Error', 'Set not found')
    else:
        messagebox.showerror('Error', 'Word and definition cannot be empty')


def main():
    root = tk.Tk()
    style = Style('superhero')
    root.title('Flashcards')
    root.geometry('400x400')
    root.resizable(False, False)

    # check for presence of data.json file
    if not pathlib.Path('data.json').exists():
        with open('data.json', 'w') as f:
            json.dump({
                'sets': {},
                'data': []
            }, f)

    with open('data.json', 'r') as file:
        try:
            data = json.load(file)
        except json.JSONDecodeError:
            data = {
                'sets': {},
                'data': []
            }


    notebook = ttk.Notebook(root)
    notebook.pack(expand=True, fill='both', padx=10, pady=5)

    set_frame = tk.Frame(notebook)
    card_frame = tk.Frame(notebook)
    review_frame = tk.Frame(notebook)

    notebook.add(set_frame, text='Set')
    notebook.add(card_frame, text='Card')
    notebook.add(review_frame, text='Review')

    set_var = tk.StringVar()

    set_option = ttk.Combobox(card_frame, textvariable=set_var)
    set_option_r = ttk.Combobox(review_frame, textvariable=set_var)

    # Set Frame
    set_label = tk.Label(set_frame, text='Set Name')
    set_label.pack(pady=8)
    set_name = tk.StringVar()
    set_entry = tk.Entry(set_frame, textvariable=set_name)
    set_entry.pack(pady=8)
    set_button = tk.Button(
        set_frame, text='Create Set', command=lambda: save_set(set_name, data, options=[set_option, set_option_r])
    )
    set_button.pack(pady=8)

    # Card Frame
    card_label = tk.Label(card_frame, text='Card', font=('Arial', 18))
    card_label.pack(pady=12)
    select_set_label = tk.Label(card_frame, text='Select Set')
    select_set_label.pack(pady=8)
    set_var.set('Select Set')
    set_option.pack(pady=8)
    options = list(data['sets'].keys())
    set_option['values'] = options
    if options:
        set_option.current(0)
    tk.Label(card_frame, text='Word').pack(pady=5)
    word = tk.StringVar()
    card_word = tk.Entry(card_frame, textvariable=word)
    card_word.pack(pady=8)
    tk.Label(card_frame, text='Definition').pack(pady=5)
    definition = tk.StringVar()
    card_definition = tk.Entry(card_frame, textvariable=definition)
    card_definition.pack(pady=8)
    card_button = tk.Button(
        card_frame, text='Save Card', command=lambda: save_card(word, definition, data, set_var.get())
    )
    card_button.pack(pady=8)

    # Review Frame
    tk.Label(review_frame, text='Review', font=('Arial', 18)).pack(pady=12)
    a = tk.Label(review_frame, text='Select Set')
    a.pack(pady=8)
    set_var.set('Select Set')
    set_option_r.pack(pady=8)
    options = list(data['sets'].keys())
    set_option_r['values'] = options
    if options:
        set_option_r.current(0)

    clicked = tk.BooleanVar(value=False)
    def show_definition():
        if not clicked.get():
            clicked.set(True)
        else:
            clicked.set(False)

    review_frame.bind('<Button-1>', lambda e: show_definition())
    if set_var.get() in data['sets']:
        a.destroy()
        set_option_r.destroy()
        cards = data['sets'][set_var.get()]
        question = tk.StringVar()
        answer = tk.StringVar()
        answer.set('')
        tk.Label(review_frame, textvariable=question).pack(pady=5)
        tk.Label(review_frame, textvariable=answer).pack(pady=5)
        for card in cards:
            question.set(card['word'])
            review_frame.wait_variable(clicked)
            answer.set(card['definition'])
            review_frame.wait_variable(clicked)
            answer.set('')

        question.set('')
        tk.Label(review_frame, text="Chipi Chipi Chapa Chapa", font=("Arial", 18)).pack(pady=5)

    root.mainloop()



if __name__ == '__main__':
    main()
    # pathlib.Path('data.json').unlink()
