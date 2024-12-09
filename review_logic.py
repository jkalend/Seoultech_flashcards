from tkinter import messagebox
import random


def review_cards_logic(set_name, data, state, word_label, definition_label, progress_label, flip_button, correct_button, wrong_button, select_set_combo, select_set_label, shuffle_button, start_button, score=None):
    if not state['cards']:
        messagebox.showinfo(
            'Info', f"You have completed all cards in this set!\nSuccess rate: {score['correct'] / (score['correct'] + score['wrong']) * 100:.2f}%")
        progress_label.config(text='Progress: 100%')
        word_label.config(text='Word: ???')
        definition_label.config(text='Definition: ???')

        flip_button.config(state='disabled')
        correct_button.config(state='disabled')
        wrong_button.config(state='disabled')

        progress_label.pack_forget()
        word_label.pack_forget()
        definition_label.pack_forget()
        flip_button.pack_forget()
        correct_button.pack_forget()
        wrong_button.pack_forget()

        select_set_label.pack(pady=8)
        select_set_combo.pack(pady=8)
        shuffle_button.pack(pady=8)
        start_button.pack(pady=8)

        if score:
            score['correct'] = 0
            score['wrong'] = 0

        return

    current_card = state['cards'][state['index']]
    if not state['flipped']:
        word_label.config(text=f"Word: {current_card['word']}")
        definition_label.config(text="Definition: ???")
        flip_button.config(state='normal')
        correct_button.config(state='disabled')
        wrong_button.config(state='disabled')
    else:
        definition_label.config(
            text=f"Definition: {current_card['definition']}")
        word_label.config(text=f"Word: {current_card['word']}")
        flip_button.config(state='disabled')
        correct_button.config(state='normal')
        wrong_button.config(state='normal')


def flip_card(state, word_label, definition_label, flip_button, correct_button, wrong_button):
    state['flipped'] = True
    review_cards_logic(None, None, state, word_label, definition_label,
                       None, flip_button, correct_button, wrong_button, None, None, None, None)


def mark_card(state, data, correct, set_name, progress_label, word_label, definition_label, flip_button, correct_button, wrong_button, select_set_combo, select_set_label, shuffle_button, start_button, score):
    if correct:
        state['cards'].pop(state['index'])
        score['correct'] += 1
    else:
        state['index'] = (state['index'] + 1) % len(state['cards'])
        score['wrong'] += 1

    total_cards = len(data['sets'][set_name])
    done = total_cards - len(state['cards'])
    progress = (done / total_cards) * 100
    progress_label.config(text=f"Progress: {progress:.2f}%")

    state['flipped'] = False

    if state['cards']:
        state['index'] %= len(state['cards'])
    review_cards_logic(set_name, data, state, word_label, definition_label,
                       progress_label, flip_button, correct_button, wrong_button, select_set_combo, select_set_label,
                       shuffle_button, start_button, score=score)


def start_review(review_set_var, data, state, review_frame, start_button, word_label, definition_label, progress_label, flip_button, correct_button, wrong_button, select_set_combo, select_set_label, shuffle_button):
    set_name = review_set_var.get()
    if set_name in data['sets'] and data['sets'][set_name]:
        state['cards'] = data['sets'][set_name].copy()
        if shuffle_button['text'] == 'Shuffle enabled':
            random.shuffle(state['cards'])
        state['index'] = 0
        state['flipped'] = False
        progress_label.config(text='Progress: 0%')

        select_set_combo.pack_forget()
        select_set_label.pack_forget()
        start_button.pack_forget()
        shuffle_button.pack_forget()

        progress_label.pack(pady=8)
        word_label.pack(pady=8)
        definition_label.pack(pady=8)

        review_cards_logic(set_name, data, state, word_label, definition_label,
                           progress_label, flip_button, correct_button, wrong_button,
                           select_set_combo, select_set_label, shuffle_button, start_button)

        flip_button.pack(side='bottom', pady=8)
        correct_button.pack(side='bottom', pady=8)
        wrong_button.pack(side='bottom', pady=8)
    else:
        messagebox.showerror('Error', 'Set is empty or not found')
        word_label.config(text='Word: ???')
        definition_label.config(text='Definition: ???')
        progress_label.config(text='Progress: 0%')
