import tkinter as tk
from tkinter import messagebox
import random

class ColorSortingGame:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Color Sorting Game")
        self.window.resizable(False, False)

        self.difficulty = None
        self.cups = []
        self.selected_cup = None
        self.moves = 0
        self.max_moves = 0

        self.colors = {
            "Easy": ["#FF6F61", "#6B5B95", "#88B04B"],
            "Medium": ["#FF6F61", "#6B5B95", "#88B04B", "#F7CAC9"],
            "Hard": ["#FF6F61", "#6B5B95", "#88B04B", "#F7CAC9", "#92A8D1"]
        }

        self.style = {
            "bg_color": "#AEEEEE",
            "button_fg": "#FFFFFF",
            "title_color": "#2F4F4F"
        }

        self.setup_main_menu()

    def setup_main_menu(self):
        self.clear_window()
        main_menu = tk.Frame(self.window, bg=self.style["bg_color"])
        main_menu.pack(expand=True, fill="both")

        title = tk.Label(
            main_menu, text="Color Sorting Game", font=("Helvetica", 32, "bold"),
            bg=self.style["bg_color"], fg=self.style["title_color"]
        )
        title.pack(pady=30)

        button_styles = {"Easy": "#FF4500", "Medium": "#4682B4", "Hard": "#8A2BE2"}
        for diff in ["Easy", "Medium", "Hard"]:
            tk.Button(
                main_menu, text=diff, font=("Helvetica", 14, "bold"), width=10,
                bg=button_styles[diff], fg=self.style["button_fg"],
                command=lambda d=diff: self.start_game(d)
            ).pack(pady=10)

        tk.Button(
            main_menu, text="How to Play", font=("Helvetica", 12), bg="#FFA500", fg=self.style["button_fg"],
            command=self.show_instructions
        ).pack(pady=20)

    def show_instructions(self):
        instructions = (
            "\u2022 Choose a difficulty.\n"
            "\u2022 Move colors between cups to sort them by color.\n"
            "\u2022 Only the topmost color of a stack can be moved.\n"
            "\u2022 Each cup can hold up to 3 colors.\n"
            "Win by grouping all colors in individual cups!"
        )
        messagebox.showinfo("How to Play", instructions)

    def start_game(self, difficulty):
        self.difficulty = difficulty
        self.moves = 0
        self.selected_cup = None
        self.clear_window()
        self.setup_game_window()

    def setup_game_window(self):
        if self.difficulty == "Easy":
            num_cups = 4
            self.max_moves = 20
            target_matches = 3
        elif self.difficulty == "Medium":
            num_cups = 5
            self.max_moves = 15
            target_matches = 4
        else:
            num_cups = 6
            self.max_moves = 12
            target_matches = 5

        self.target_matches = target_matches

        game_frame = tk.Frame(self.window, bg=self.style["bg_color"])
        game_frame.pack(expand=True, fill="both", padx=20, pady=20)

        self.status_label = tk.Label(
            game_frame, text="Select a cup to start", font=("Helvetica", 14),
            bg=self.style["bg_color"], fg=self.style["title_color"]
        )
        self.status_label.pack(pady=5)

        self.moves_label = tk.Label(
            game_frame, text=f"Moves: 0/{self.max_moves}", font=("Helvetica", 14),
            bg=self.style["bg_color"], fg=self.style["title_color"]
        )
        self.moves_label.pack(pady=5)

        self.cups = [[] for _ in range(num_cups)]
        colors = self.colors[self.difficulty] * 3
        random.shuffle(colors)

        for i in range(num_cups - 1):
            self.cups[i] = colors[i * 3:(i + 1) * 3]

        cups_frame = tk.Frame(game_frame, bg=self.style["bg_color"])
        cups_frame.pack()
        self.cup_buttons = []
        for i in range(num_cups):
            cup_frame = tk.Frame(
                cups_frame, width=80, height=240, bg="#FFFFFF", relief="solid", bd=2
            )
            cup_frame.grid(row=0, column=i, padx=10, pady=5)

            tk.Label(
                cups_frame, text=f"Cup {i + 1}", font=("Helvetica", 12), bg=self.style["bg_color"]
            ).grid(row=1, column=i)

            btn = tk.Button(
                cups_frame, text="Select", font=("Helvetica", 10), bg="#FFA500",
                command=lambda idx=i: self.select_cup(idx)
            )
            btn.grid(row=2, column=i)
            self.cup_buttons.append(cup_frame)

        self.update_cups_display()

        controls_frame = tk.Frame(game_frame, bg=self.style["bg_color"])
        controls_frame.pack(pady=10)

        tk.Button(
            controls_frame, text="Main Menu", command=self.setup_main_menu,
            font=("Helvetica", 12), bg="#FFA500", fg=self.style["button_fg"]
        ).pack(side=tk.LEFT, padx=10)

        tk.Button(
            controls_frame, text="Restart", command=lambda: self.start_game(self.difficulty),
            font=("Helvetica", 12), bg="#FFA500", fg=self.style["button_fg"]
        ).pack(side=tk.LEFT, padx=10)

    def select_cup(self, index):
        if self.selected_cup is None:
            if self.cups[index]:
                self.selected_cup = index
                self.status_label.config(text=f"Selected Cup {index + 1}. Choose destination.")
            else:
                self.status_label.config(text="Cannot select an empty cup!")
        else:
            if self.selected_cup == index:
                self.selected_cup = None
                self.status_label.config(text="Selection cancelled.")
            else:
                self.move_color(self.selected_cup, index)

    def move_color(self, from_cup, to_cup):
        if len(self.cups[to_cup]) >= 3:
            self.status_label.config(text="Destination cup is full! You lose.")
            self.show_popup("You lost: Cup overflowed!", win=False)
            return

        color = self.cups[from_cup].pop()
        self.cups[to_cup].append(color)
        self.moves += 1
        self.moves_label.config(text=f"Moves: {self.moves}/{self.max_moves}")
        self.selected_cup = None

        self.update_cups_display()
        self.check_conditions()

    def update_cups_display(self):
        for i, cup in enumerate(self.cups):
            for widget in self.cup_buttons[i].winfo_children():
                widget.destroy()

            for color in reversed(cup):
                tk.Frame(
                    self.cup_buttons[i], bg=color, width=60, height=20
                ).pack(pady=2)

    def check_conditions(self):
        valid_cups = sum(1 for cup in self.cups if len(cup) == 3 and len(set(cup)) == 1)

        if valid_cups >= self.target_matches:
            self.show_popup("Congrats! You Matched All the Colors", win=True)
        elif self.moves >= self.max_moves:
            self.show_popup("Game Over: Out of moves! Try again.", win=False)

    def show_popup(self, message, win):
        result = messagebox.askquestion(
            "Congratulations" if win else "Game Over",
            f"{message}\nPlay again?",
            icon="info"
        )
        if result == "yes":
            self.start_game(self.difficulty)
        else:
            self.setup_main_menu()

    def clear_window(self):
        for widget in self.window.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    game = ColorSortingGame()
    game.window.mainloop()
