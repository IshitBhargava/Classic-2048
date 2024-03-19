import tkinter as tk
import random
import sounddevice as sd    # To produce the audible buzz sound
import numpy as np          # It is needed to work with arrays

def generate_buzz(duration_ms=10, frequency=440):
    sample_rate = 44100                                                                   # Sample rate in Hz
    t = np.linspace(0, duration_ms / 1000, int(sample_rate * duration_ms / 1000), False)  # Time array
    signal = np.sin(2 * np.pi * frequency * t)                                            # Generate a sine wave signal
    audio = (signal * 32767).astype(np.int16)                                             # Convert to 16-bit integer PCM
    sd.play(audio, samplerate=sample_rate)                                                # Play the audio

class Game2048(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("2048")
        self.geometry("400x400")
        self.board = [[0] * 4 for _ in range(4)]
        self.tiles = []
        self.create_board()
        self.add_new_tile()
        self.bind("<Key>", self.handle_keypress)

    def create_board(self):
        for i in range(4):
            row = []
            for j in range(4):
                tile = tk.Label(self, text="", font=("Arial", 20), width=5, height=2, borderwidth=2, relief="ridge")
                tile.grid(row=i, column=j, padx=5, pady=5)
                row.append(tile)
            self.tiles.append(row)

    def add_new_tile(self):
        empty_cells = [(i, j) for i in range(4) for j in range(4) if self.board[i][j] == 0]
        if empty_cells:
            i, j = random.choice(empty_cells)
            self.board[i][j] = 2 if random.random() < 0.9 else 4
            self.update_board()

    def update_board(self):
        for i in range(4):
            for j in range(4):
                value = self.board[i][j]
                self.tiles[i][j]["text"] = str(value) if value != 0 else ""
                self.tiles[i][j]["bg"] = self.get_tile_color(value)

    def get_tile_color(self, value):
        colors = {
            2: "green",
            4: "blue",
            8: "red",
            16: "yellow",
            32: "purple",
            64: "cyan",
            128: "pink",
            256: "orange"
        }
        return colors.get(value, "white")

    def handle_keypress(self, event):
        if event.keysym in {"Up", "Down", "Left", "Right"}:
            self.move_tiles(event.keysym)
            self.add_new_tile()
            self.custom_function()

    def move_tiles(self, direction):
        if direction == "Up":
            self.board = self.transpose_board(self.board)
            self.board = self.move_left(self.board)
            self.board = self.transpose_board(self.board)
        elif direction == "Down":
            self.board = self.transpose_board(self.board)
            self.board = self.reverse_rows(self.board)
            self.board = self.move_left(self.board)
            self.board = self.reverse_rows(self.board)
            self.board = self.transpose_board(self.board)
        elif direction == "Left":
            self.board = self.move_left(self.board)
        elif direction == "Right":
            self.board = self.reverse_rows(self.board)
            self.board = self.move_left(self.board)
            self.board = self.reverse_rows(self.board)
        self.update_board()

    def move_left(self, board):
        new_board = []
        for row in board:
            new_row = []
            last_value = 0
            for value in row:
                if value != 0:
                    if value == last_value:
                        new_row[-1] *= 2
                        last_value = 0
                    else:
                        new_row.append(value)
                        last_value = value
            new_row += [0] * (4 - len(new_row))
            new_board.append(new_row)
        return new_board

    def reverse_rows(self, board):
        return [row[::-1] for row in board]

    def transpose_board(self, board):
        return [list(row) for row in zip(*board)]

    def custom_function(self):
        # Implement your custom function here
        #print("Custom function called!")
        generate_buzz()

if __name__ == "__main__":
    game = Game2048()
    game.mainloop()
