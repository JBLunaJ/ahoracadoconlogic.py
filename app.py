from logic import *

# Definir la palabra a adivinar
word = "ONOMATOPEYA"

# Definir las letras posibles manualmente
letters = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]

# Inicializar conocimiento
knowledge = And()

# Agregar proposiciones para cada letra de la palabra
for letter in set(word):
    knowledge.add(Symbol(f"Letter{letter}"))

# Solo se puede tener una ocurrencia de cada letra
for letter in letters:
    for letter1 in letters:
        if letter != letter1:
            knowledge.add(Implication(Symbol(f"Letter{letter}"), Not(Symbol(f"Letter{letter1}"))))

# Función para comprobar el modelo y mostrar resultados
def check_knowledge(knowledge, letters):
    possible_letters = []
    for letter in letters:
        symbol = Symbol(f"Letter{letter}")
        if model_check(knowledge, symbol):
            possible_letters.append(letter)
    return possible_letters

# Mostrar la palabra adivinada
def display_word(guesses):
    displayed = ""
    for letter in word:
        if letter in guesses:
            displayed += letter + " "
        else:
            displayed += "_ "
    return displayed.strip()

# Juego principal
print("Bienvenido al juego de ahorcados!")

# Definir letras incorrectas y correctas
incorrect_letters = []
correct_letters = []
max_attempts = 5  # Número máximo de intentos fallidos
attempts = 0  # Contador de intentos fallidos

while True:
    print(f"Palabra: {display_word(correct_letters)}")
    print(f"Letras incorrectas: {', '.join(incorrect_letters) if incorrect_letters else 'Ninguna'}")
    
    guess = input("Ingresa una letra (A-Z) o 'salir' para terminar: ").upper()

    if guess == "SALIR":
        print("Juego terminado.")
        break
    elif guess not in letters or len(guess) != 1:
        print("Por favor, ingresa una letra válida.")
        continue

    # Verificar si la letra ya fue adivinada
    if guess in incorrect_letters or guess in correct_letters:
        print(f"La letra '{guess}' ya fue ingresada. Intenta otra.")
        continue

    # Agregar letra incorrecta si no está en la palabra
    if guess not in word:
        incorrect_letters.append(guess)
        attempts += 1  # Incrementar el contador de intentos fallidos
        knowledge.add(Not(Symbol(f"Letter{guess}")))
        print(f"Letras incorrectas: {', '.join(incorrect_letters)}")
        if attempts >= max_attempts:  # Comprobar si se alcanzó el límite de intentos
            print(f"¡Has alcanzado el límite de intentos! La palabra era: {word}")
            break
    else:
        correct_letters.append(guess)
        knowledge.add(Symbol(f"Letter{guess}"))

    # Verificar si se ha adivinado toda la palabra
    if all(letter in correct_letters for letter in set(word)):
        print(f"¡Felicidades! Has adivinado la palabra: {word}")
        break

# Fin del juego
print(f"La palabra era: {word}")
