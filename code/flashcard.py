import tkinter as tk
from tkinter import messagebox, filedialog
from tkmacosx import Button  # For macOS button color handling
import random
import json

class FlashcardApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Flashcards")
        self.root.geometry("800x600")
        self.root.config(bg="#ffffff")  # Change the whole app background to white

        # Flashcard data
        self.flashcards = []
        self.current_card = None
        self.is_flipped = False
        self.current_index = 0

        # Force DPI scaling for macOS
        if self.root.tk.call('tk', 'windowingsystem') == 'aqua':
            self.root.tk.call('tk', 'scaling', 2.0)

        # Create a main frame to hold all widgets, center it with pack
        self.main_frame = tk.Frame(self.root, bg="#ffffff")  # Main frame background also white
        self.main_frame.pack(expand=True, anchor="center")

        # Flashcard display area (like a card)
        self.card_frame_container = tk.Frame(self.main_frame, bg="#ffffff")  # Dedicated container for the card
        self.card_frame_container.pack()

        self.card_frame = tk.Frame(self.card_frame_container, bg="#ffffff", width=750, height=400, bd=5, relief="solid", highlightbackground="#ddd", highlightthickness=2)
        self.card_frame.pack()

        self.card_label = tk.Label(self.card_frame, text="Click Add to add a flashcard", font=("Arial", 24),
                                   wraplength=500, bg="white", fg="#333", padx=20, pady=20)
        self.card_label.place(relwidth=1, relheight=1)

        # Static Card number display (ticker) – same as buttons
        self.ticker_frame = tk.Frame(self.root, bg="#ffffff")  # Static frame for the ticker
        self.ticker_frame.pack()

        self.card_number_label = tk.Label(self.ticker_frame, text="0 / 0", font=("Arial", 14), bg="#ffffff", fg="#333")
        self.card_number_label.pack(pady=10)

        # Buttons Frame – stays static like the ticker
        self.button_frame = tk.Frame(self.root, bg="#ffffff")  # Separate frame for buttons to keep them static
        self.button_frame.pack()

        # Custom button styles (all buttons have baby blue color)
        button_color = "#87CEEB"  # Baby blue color for all buttons

        self.add_button = Button(self.button_frame, text="Add Flashcard", command=self.add_flashcard, 
                                 bg=button_color, fg="white", font=("Arial", 12), borderless=1, 
                                 activebackground="#5DACD8", activeforeground="white")
        self.add_button.pack(side="left", padx=10, pady=10)

        self.edit_button = Button(self.button_frame, text="Edit Flashcard", command=self.edit_flashcard_popup,
                                  bg=button_color, fg="white", font=("Arial", 12), borderless=1, 
                                  activebackground="#5DACD8", activeforeground="white")
        self.edit_button.pack(side="left", padx=10, pady=10)

        self.flip_button = Button(self.button_frame, text="Flip", command=self.flip_flashcard_with_animation,
                                  bg=button_color, fg="white", font=("Arial", 12), borderless=1, 
                                  activebackground="#5DACD8", activeforeground="white")
        self.flip_button.pack(side="left", padx=10, pady=10)

        self.next_button = Button(self.button_frame, text="Next", command=self.next_flashcard, 
                                  bg=button_color, fg="white", font=("Arial", 12), borderless=1, 
                                  activebackground="#5DACD8", activeforeground="white")
        self.next_button.pack(side="left", padx=10, pady=10)

        self.prev_button = Button(self.button_frame, text="Previous", command=self.prev_flashcard, 
                                  bg=button_color, fg="white", font=("Arial", 12), borderless=1, 
                                  activebackground="#5DACD8", activeforeground="white")
        self.prev_button.pack(side="left", padx=10, pady=10)

        self.save_button = Button(self.button_frame, text="Save", command=self.save_flashcards,
                                  bg=button_color, fg="white", font=("Arial", 12), borderless=1, 
                                  activebackground="#5DACD8", activeforeground="white")
        self.save_button.pack(side="left", padx=10, pady=10)

        self.load_button = Button(self.button_frame, text="Load", command=self.load_flashcards,
                                  bg=button_color, fg="white", font=("Arial", 12), borderless=1, 
                                  activebackground="#5DACD8", activeforeground="white")
        self.load_button.pack(side="left", padx=10, pady=10)

        self.randomize_button = Button(self.button_frame, text="Randomize", command=self.randomize_flashcards,
                                       bg=button_color, fg="white", font=("Arial", 12), borderless=1, 
                                       activebackground="#5DACD8", activeforeground="white")
        self.randomize_button.pack(side="left", padx=10, pady=10)

    def add_flashcard(self):
        self.custom_popup()

    def custom_popup(self):
        popup = tk.Toplevel(self.root)
        popup.geometry("500x700")
        popup.title("Add Flashcard")
        popup.config(bg="#ffffff")  # Set the background color of the pop-up to white

        button_color = "#87CEEB"

        tk.Label(popup, text="Front Text:", font=("Arial", 14), bg="#ffffff").pack(pady=10)
        front_text = tk.Text(popup, width=60, height=5, font=("Arial", 14), wrap="word")
        front_text.pack(pady=10)

        tk.Label(popup, text="Back Text:", font=("Arial", 14), bg="#ffffff").pack(pady=10)
        back_text = tk.Text(popup, width=60, height=5, font=("Arial", 14), wrap="word")
        back_text.pack(pady=10)

        save_button = Button(popup, text="Save", bg=button_color, fg="white", font=("Arial", 12), borderless=1, 
                             activebackground="#5DACD8", command=lambda: self.save_new_flashcard(popup, front_text.get("1.0", tk.END).strip(), back_text.get("1.0", tk.END).strip()))
        save_button.pack(pady=20)

    def save_new_flashcard(self, popup, front, back):
        if front and back:
            self.flashcards.append({"front": front, "back": back})
            self.show_card(len(self.flashcards) - 1)
            popup.destroy()
        else:
            messagebox.showwarning("Input Error", "Both front and back text must be provided")

    def show_card(self, index):
        if 0 <= index < len(self.flashcards):
            self.current_index = index
            self.is_flipped = False
            self.update_card_text(self.flashcards[index]['front'])
            self.update_card_number()

    def edit_flashcard_popup(self):
        if self.flashcards:
            flashcard = self.flashcards[self.current_index]

            popup = tk.Toplevel(self.root)
            popup.geometry("500x700")
            popup.title("Edit Flashcard")
            popup.config(bg="#ffffff")

            button_color = "#87CEEB"

            tk.Label(popup, text="Edit Front Text:", font=("Arial", 14), bg="#ffffff").pack(pady=10)
            front_text = tk.Text(popup, width=60, height=5, font=("Arial", 14), wrap="word")
            front_text.insert(tk.END, flashcard['front'])
            front_text.pack(pady=10)

            tk.Label(popup, text="Edit Back Text:", font=("Arial", 14), bg="#ffffff").pack(pady=10)
            back_text = tk.Text(popup, width=60, height=5, font=("Arial", 14), wrap="word")
            back_text.insert(tk.END, flashcard['back'])
            back_text.pack(pady=10)

            # Save changes
            save_button = Button(popup, text="Save Changes", bg=button_color, fg="white", font=("Arial", 12), borderless=1, 
                                 activebackground="#5DACD8", command=lambda: self.save_edited_flashcard(popup, front_text.get("1.0", tk.END).strip(), back_text.get("1.0", tk.END).strip()))
            save_button.pack(pady=10)

            # Remove the flashcard
            remove_button = Button(popup, text="Remove Flashcard", bg="red", fg="white", font=("Arial", 12), borderless=1, 
                                   activebackground="darkred", command=lambda: self.remove_flashcard(popup))
            remove_button.pack(pady=10)

    def save_edited_flashcard(self, popup, new_front, new_back):
        if new_front and new_back:
            self.flashcards[self.current_index] = {"front": new_front, "back": new_back}
            self.show_card(self.current_index)
            popup.destroy()
        else:
            messagebox.showwarning("Input Error", "Both front and back text must be provided")

    def remove_flashcard(self, popup):
        if messagebox.askyesno("Remove Flashcard", "Are you sure you want to remove this flashcard?"):
            del self.flashcards[self.current_index]
            if self.flashcards:
                self.show_card(0)
            else:
                self.card_label.config(text="No Flashcards Available", font=("Arial", 24))
                self.card_number_label.config(text="0 / 0")
            popup.destroy()

    def flip_flashcard(self):
        if self.flashcards:
            self.is_flipped = not self.is_flipped
            card_text = self.flashcards[self.current_index]['back'] if self.is_flipped else self.flashcards[self.current_index]['front']
            self.update_card_text(card_text)
            self.card_frame.config(highlightbackground="#FF9800" if self.is_flipped else "#4CAF50")

    def flip_flashcard_with_animation(self):
        if self.flashcards:
            self.animate_flip(400, 0, 40, lambda: self.flip_flashcard())  # Faster with step 40

    def animate_flip(self, start_height, end_height, step, callback):
        # Flip card animation from bottom to top with faster speed
        if start_height == end_height:
            if callback:
                callback()
            self.root.after(10, lambda: self.animate_flip(end_height, 400, step, None))  # Faster expansion
        elif start_height > end_height:
            new_height = start_height - step
            self.card_frame.config(height=new_height)
            self.root.after(5, lambda: self.animate_flip(new_height, end_height, step, callback))  # Faster shrink
        elif start_height < end_height:
            new_height = start_height + step
            self.card_frame.config(height=new_height)
            self.root.after(5, lambda: self.animate_flip(new_height, end_height, step, callback))  # Faster expansion

    def next_flashcard(self):
        if self.flashcards:
            self.current_index = (self.current_index + 1) % len(self.flashcards)
            self.show_card(self.current_index)

    def prev_flashcard(self):
        if self.flashcards:
            self.current_index = (self.current_index - 1) % len(self.flashcards)
            self.show_card(self.current_index)

    def update_card_text(self, text):
        self.card_label.config(text=text, font=("Arial", 24, "bold"), fg="#333")

    def update_card_number(self):
        total_cards = len(self.flashcards)
        self.card_number_label.config(text=f"{self.current_index + 1} / {total_cards}" if total_cards > 0 else "0 / 0")

    def save_flashcards(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".json",
                                                 filetypes=[("JSON files", "*.json"), ("All files", "*.*")])
        if file_path:
            with open(file_path, 'w') as f:
                json.dump(self.flashcards, f)
            messagebox.showinfo("Save", "Flashcards saved successfully!")

    def load_flashcards(self):
        file_path = filedialog.askopenfilename(defaultextension=".json",
                                               filetypes=[("JSON files", "*.json"), ("All files", "*.*")])
        if file_path:
            try:
                with open(file_path, 'r') as f:
                    loaded_flashcards = json.load(f)

                replace = messagebox.askyesno("Replace or Append", "Do you want to replace the current flashcards? (Click 'No' to append)")

                if replace:
                    self.flashcards = loaded_flashcards
                else:
                    self.flashcards.extend(loaded_flashcards)

                self.show_card(0)
                messagebox.showinfo("Load", "Flashcards loaded successfully!")
            except FileNotFoundError:
                messagebox.showerror("Error", "No saved flashcards found!")
            except json.JSONDecodeError:
                messagebox.showerror("Error", "Error loading flashcards. File might be corrupted.")

    def randomize_flashcards(self):
        if self.flashcards:
            random.shuffle(self.flashcards)
            self.current_index = 0
            self.show_card(self.current_index)

if __name__ == "__main__":
    root = tk.Tk()
    app = FlashcardApp(root)
    root.mainloop()
