import tkinter as tk
from tkinter import messagebox
from logic import *
import random
from PIL import Image, ImageTk

class HangmanApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Juego de Ahorcado")

        # Inicialmente sin palabra seleccionada
        self.word = None
        self.knowledge = None
        self.victories = 0
        self.losses = 0

        # Crear botones para seleccionar dificultad
        self.difficulty_frame = tk.Frame(root)
        self.difficulty_frame.pack(pady=20)

        self.easy_button = tk.Button(self.difficulty_frame, text="Fácil", command=lambda: self.set_difficulty("facil"))
        self.easy_button.pack(side="left", padx=10)

        self.medium_button = tk.Button(self.difficulty_frame, text="Intermedio", command=lambda: self.set_difficulty("intermedio"))
        self.medium_button.pack(side="left", padx=10)

        self.hard_button = tk.Button(self.difficulty_frame, text="Difícil", command=lambda: self.set_difficulty("dificil"))
        self.hard_button.pack(side="left", padx=10)

        # Imagen del ahorcado
        self.image_label = tk.Label(root)
        self.image_label.pack(pady=20)
        self.update_image(0)  # Estado inicial

        # Label para mostrar la palabra
        self.word_label = tk.Label(root, text="", font=("Helvetica", 18))
        self.word_label.pack(pady=20)

        # Entry para ingresar letras (desactivado hasta que se seleccione la dificultad)
        self.letter_entry = tk.Entry(root, state="disabled")
        self.letter_entry.pack(pady=10)
        self.letter_entry.bind('<Return>', self.check_guess)

        # Botón para adivinar (desactivado hasta que se seleccione la dificultad)
        self.guess_button = tk.Button(root, text="Adivinar", command=self.check_guess, state="disabled")
        self.guess_button.pack(pady=10)

        # Label para mostrar letras incorrectas
        self.incorrect_label = tk.Label(root, text="Letras incorrectas: Ninguna", font=("Helvetica", 12))
        self.incorrect_label.pack(pady=20)

        # Contadores de victorias y derrotas
        self.score_label = tk.Label(root, text="Victorias: 0 | Derrotas: 0", font=("Helvetica", 12))
        self.score_label.pack(pady=10)

        # Botones de reinicio y salir
        self.button_frame = tk.Frame(root)
        self.button_frame.pack(pady=20)

        self.reset_button = tk.Button(self.button_frame, text="Reiniciar", command=self.reset_game, state="disabled")
        self.reset_button.pack(side="left", padx=10)

        self.exit_button = tk.Button(self.button_frame, text="Salir", command=root.quit)
        self.exit_button.pack(side="left", padx=10)

        # Inicializar otras variables
        self.correct_letters = []
        self.incorrect_letters = []
        self.max_attempts = 5
        self.attempts = 0

    def set_difficulty(self, difficulty):
        # Cargar las palabras desde los archivos correspondientes según la dificultad elegida
        if difficulty == "facil":
            file_name = "txts/facil.txt"
        elif difficulty == "intermedio":
            file_name = "txts/intermedio.txt"
        else:
            file_name = "txts/dificil.txt"

        with open(file_name, "r") as file:
            word_list = file.read().splitlines()

        # Elegir una palabra aleatoria de la lista
        self.word = random.choice(word_list).upper()

        # Inicializar conocimiento
        self.knowledge = And()

        for letter in set(self.word):
            self.knowledge.add(Symbol(f"Letter{letter}"))

        for letter in letters:
            for letter1 in letters:
                if letter != letter1:
                    self.knowledge.add(Implication(Symbol(f"Letter{letter}"), Not(Symbol(f"Letter{letter1}"))))

        # Habilitar los elementos de juego
        self.word_label.config(text=self.display_word())
        self.letter_entry.config(state="normal")
        self.guess_button.config(state="normal")
        self.reset_button.config(state="disabled")

        # Desactivar los botones de dificultad
        self.easy_button.config(state="disabled")
        self.medium_button.config(state="disabled")
        self.hard_button.config(state="disabled")

    def display_word(self):
        displayed = ""
        for letter in self.word:
            if letter in self.correct_letters:
                displayed += letter + " "
            else:
                displayed += "_ "
        return displayed.strip()

    def check_guess(self, event=None):
        guess = self.letter_entry.get().upper()
        self.letter_entry.delete(0, tk.END)

        if guess not in letters or len(guess) != 1:
            messagebox.showerror("Error", "Por favor, ingresa una letra válida.")
            return

        if guess in self.correct_letters or guess in self.incorrect_letters:
            messagebox.showwarning("Advertencia", f"La letra '{guess}' ya fue ingresada.")
            return

        if guess in self.word:
            self.correct_letters.append(guess)
            self.knowledge.add(Symbol(f"Letter{guess}"))
            self.word_label.config(text=self.display_word())
            if all(letter in self.correct_letters for letter in set(self.word)):
                self.victories += 1
                self.score_label.config(text=f"Victorias: {self.victories} | Derrotas: {self.losses}")
                messagebox.showinfo("Ganaste", f"¡Felicidades! Has adivinado la palabra: {self.word}")
                self.end_game()
        else:
            self.incorrect_letters.append(guess)
            self.attempts += 1
            self.knowledge.add(Not(Symbol(f"Letter{guess}")))
            self.incorrect_label.config(text=f"Letras incorrectas: {', '.join(self.incorrect_letters)}")
            self.update_image(self.attempts)
            if self.attempts >= self.max_attempts:
                self.losses += 1
                self.score_label.config(text=f"Victorias: {self.victories} | Derrotas: {self.losses}")
                messagebox.showerror("Perdiste", f"¡Has alcanzado el límite de intentos! La palabra era: {self.word}")
                self.end_game()

    def update_image(self, attempt):
        image_path = f"imagenes/hangman{attempt}.png"
        image = Image.open(image_path)
        image = image.resize((200, 200), Image.Resampling.LANCZOS)
        photo = ImageTk.PhotoImage(image)
        self.image_label.config(image=photo)
        self.image_label.image = photo  # Keep a reference!

    def end_game(self):
        self.letter_entry.config(state="disabled")
        self.guess_button.config(state="disabled")
        self.reset_button.config(state="normal")

    def reset_game(self):
        self.correct_letters = []
        self.incorrect_letters = []
        self.attempts = 0
        self.update_image(0)
        self.word_label.config(text="")
        self.incorrect_label.config(text="Letras incorrectas: Ninguna")

        # Reactivar los botones de dificultad
        self.easy_button.config(state="normal")
        self.medium_button.config(state="normal")
        self.hard_button.config(state="normal")
        self.reset_button.config(state="disabled")

if __name__ == "__main__":
    root = tk.Tk()
    letters = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
    app = HangmanApp(root)
    root.mainloop()
