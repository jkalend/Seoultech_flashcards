from tkinter import messagebox
from data_handler import save_data


def save_set(entry, data, **kwargs):
    set_name = entry.get()
    if set_name:
        if set_name not in data['sets']:
            data['sets'][set_name] = []
            save_data(data)
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
            save_data(data)
            messagebox.showinfo('Success', 'Card saved successfully')
            word.set('')
            definition.set('')
        except KeyError:
            messagebox.showerror(
                'Error', 'Set not found. Please select a valid set.')
            card_set_combo['values'] = list(data['sets'].keys())
    else:
        messagebox.showerror('Error', 'Word and definition cannot be empty')
