import json
import pathlib
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from ttkbootstrap import Style


def save_set(entry, data, **kwargs):
    set_name = entry.get()
    if set_name:
        if set_name not in data['sets']:
            data['sets'][set_name] = []
            with open('data.json', 'w') as file:
                json.dump(data, file)
            messagebox.showinfo('Success', f'Set "{
                                set_name}" saved successfully')
            if 'options' in kwargs:
                for option in kwargs['options']:
                    option['values'] = list(data['sets'].keys())
        else:
            messagebox.showerror('Error', f'Set "{set_name}" already exists')
    else:
        messagebox.showerror('Error', 'Set name cannot be empty')
    entry.set('')


def save_card(word, definition, data, set_name, card_set_combo):
    card_word = word.get()
    card_definition = definition.get()
    if card_word and card_definition:
        try:
            data['sets'][set_name].append(
                {'word': card_word, 'definition': card_definition})
            with open('data.json', 'w') as file:
                json.dump(data, file)
            messagebox.showinfo('Success', 'Card saved successfully')
            word.set('')
            definition.set('')
        except KeyError:
            messagebox.showerror(
                'Error', 'Set not found. Please select a valid set.')
            card_set_combo['values'] = list(data['sets'].keys())
    else:
        messagebox.showerror('Error', 'Word and definition cannot be empty')


def review_cards_logic(set_name, data, state, word_label, definition_label, progress_label, flip_button, correct_button, wrong_button):
    """
    Display the current card in the review process.
    """
    if not state['cards']:
        messagebox.showinfo(
            'Info', 'You have completed all cards in this set!')
        progress_label.config(text='Progress: 100%')
        word_label.config(text='Word: ???')
        definition_label.config(text='Definition: ???')

        flip_button.config(state='disabled')
        correct_button.config(state='disabled')
        wrong_button.config(state='disabled')
        return

    current_card = state['cards'][state['index']]
    if not state['flipped']:
        # Show word
        word_label.config(text=f"Word: {current_card['word']}")
        definition_label.config(text="Definition: ???")
        flip_button.config(state='normal')
        correct_button.config(state='disabled')
        wrong_button.config(state='disabled')
    else:
        # Show definition after flip
        definition_label.config(
            text=f"Definition: {current_card['definition']}")
        word_label.config(text="Word: ???")
        flip_button.config(state='disabled')
        correct_button.config(state='normal')
        wrong_button.config(state='normal')


def flip_card(state, word_label, definition_label, flip_button, correct_button, wrong_button):
    """
    Flip the card to reveal the definition.
    """
    state['flipped'] = True
    review_cards_logic(
        None, None, state, word_label, definition_label, None, flip_button, correct_button, wrong_button
    )


def mark_card(state, data, correct, set_name, progress_label, word_label, definition_label, flip_button, correct_button, wrong_button):
    """
    Mark the card as correct or wrong and move to the next card.
    """
    if correct:
        # Remove the current card if marked correct
        state['cards'].pop(state['index'])
    else:
        # Move to the next card, and keep the current card
        state['index'] = (state['index'] + 1) % len(state['cards'])

    total_cards = len(data['sets'][set_name])
    done = total_cards - len(state['cards'])
    progress = (done / total_cards) * 100
    progress_label.config(text=f"Progress: {progress:.2f}%")

    state['flipped'] = False

    if state['cards']:
        # Move to the next card
        state['index'] %= len(state['cards'])
    review_cards_logic(
        set_name, data, state, word_label, definition_label, progress_label, flip_button, correct_button, wrong_button
    )


def start_review(review_set_var, data, state, review_frame, start_button, word_label, definition_label, progress_label, flip_button, correct_button, wrong_button, select_set_combo, select_set_label):
    """
    Start the review process by showing the review screen.
    """
    set_name = review_set_var.get()
    if set_name in data['sets'] and data['sets'][set_name]:
        state['cards'] = data['sets'][set_name].copy()
        state['index'] = 0
        state['flipped'] = False
        progress_label.config(text='Progress: 0%')

        select_set_combo.pack_forget()
        select_set_label.pack_forget()
        start_button.pack_forget()

        progress_label.pack(pady=8)
        word_label.pack(pady=8)
        definition_label.pack(pady=8)

        # Display first card
        review_cards_logic(
            set_name, data, state, word_label, definition_label, progress_label, flip_button, correct_button, wrong_button
        )

        flip_button.pack(side=tk.BOTTOM, pady=8)
        correct_button.pack(side=tk.BOTTOM, pady=8)
        wrong_button.pack(side=tk.BOTTOM, pady=8)
    else:
        messagebox.showerror('Error', 'Set is empty or not found')
        word_label.config(text='Word: ???')
        definition_label.config(text='Definition: ???')
        progress_label.config(text='Progress: 0%')


def main():
    root = tk.Tk()
    style = Style('superhero')
    root.title('Flashcards')
    root.geometry('400x400')
    root.resizable(False, False)

    if not pathlib.Path('data.json').exists():
        with open('data.json', 'w') as f:
            json.dump({'sets': {}, 'data': []}, f)

    with open('data.json', 'r') as file:
        try:
            data = json.load(file)
        except json.JSONDecodeError:
            data = {'sets': {}, 'data': []}

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
    ttk.Button(
        set_frame,
        text='Create Set',
        command=lambda: save_set(set_name_var, data, options=[
                                 card_set_combo, review_set_combo])
    ).pack(pady=8)

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
    ttk.Button(
        card_frame,
        text='Save Card',
        command=lambda: save_card(
            word_var, definition_var, data, card_set_var.get(), card_set_combo)
    ).pack(pady=8)

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

    flip_button = ttk.Button(
        review_frame, text="Flip", state='disabled', command=lambda: flip_card(state, word_label, definition_label, flip_button, correct_button, wrong_button)
    )

    correct_button = ttk.Button(
        review_frame,
        text='Correct',
        state='disabled',
        command=lambda: mark_card(state, data, True, review_set_var.get(
        ), progress_label, word_label, definition_label, flip_button, correct_button, wrong_button)
    )

    wrong_button = ttk.Button(
        review_frame,
        text='Wrong',
        state='disabled',
        command=lambda: mark_card(state, data, False, review_set_var.get(
        ), progress_label, word_label, definition_label, flip_button, correct_button, wrong_button)
    )

    root.mainloop()


if __name__ == '__main__':
    main()

    # pathlib.Path('data.json').unlink()
