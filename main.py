import random

def load_words():
    with open("words.txt", 'r') as input_file:
        line = input_file.readline()
        list_of_words = line.split()

    return list_of_words

def is_word_guessed(secret_word, letters_guessed):
    return all(char in letters_guessed for char in secret_word)

def get_guessed_word(secret_word, letters_guessed):
    guessed_word = ''
    for char in secret_word:
        if char in letters_guessed:
            guessed_word += char + " "
        else:
            guessed_word += "_ "

    return guessed_word.rstrip()

def get_available_letters(letters_guessed):
    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    not_guessed = [char for char in alphabet if char not in letters_guessed]

    return ''.join(not_guessed)

def update_drawing(drawing, available_guesses):
    drawing_dict = {
        5: (1, '|        |'),
        4: (2, '|        O'),
        3: (3, '|        | '),
        2: (4, '|      / | \ '),
        1: (5, '|        |    '),
        0: (6, '|      / | \ ')
    }

    if available_guesses == 6:
        for i in drawing:
            print(i, end='\n')
    elif available_guesses < 6:
        for idx in range(5, available_guesses - 1, -1):
            drawing[drawing_dict[idx][0]] = drawing_dict[idx][1]
        for i in drawing:
            print(i, end='\n')

    return drawing

def hangman(secret_word):
    drawing = [
        '__________',  # idx 0
        '|         ',  # idx 1
        '|         ',
        '|         ',
        '|         ',
        '|         ',
        '|         ',  # idx 6
        '|         ',
    ]

    avail_guesses = 6
    guessed_letters = []
    warnings = 3
    spacer = '>>>>>>>>>>>>>>>>>>>>>>>>'

    print('¡Bienvenido al juego del Ahorcado!')
    print(f'Estoy pensando en una palabra que tiene {len(secret_word)} letras.')
    print(f'Tienes {warnings} advertencias disponibles.')
    print(spacer)

    is_winner_found = False

    while avail_guesses > 0:
        if not is_winner_found:
            update_drawing(drawing, avail_guesses)
            current_guess = get_guessed_word(secret_word, guessed_letters)
            avail_letters = get_available_letters(guessed_letters)

            print(f'Te quedan {avail_guesses} intentos.')
            print('Letras disponibles:', avail_letters)

            user_guess = input('Por favor, adivina una letra: ')

            if user_guess.lower() in secret_word and user_guess.lower() not in guessed_letters:
                guessed_letters.append(user_guess.lower())
                current_guess = get_guessed_word(secret_word, guessed_letters)

                print('¡Buena elección!', current_guess)
            else:
                if user_guess.isalpha() and user_guess.lower() not in guessed_letters:
                    if user_guess in 'aeiou':
                        avail_guesses -= 2
                    else:
                        avail_guesses -= 1

                    guessed_letters.append(user_guess.lower())
                    print('¡Ups! Esa letra no está en mi palabra:', current_guess)
                else:
                    if warnings > 0:
                        warnings -= 1
                        if user_guess in guessed_letters:
                            print("¡Ups! Ya has adivinado esa letra.")
                        else:
                            print('¡Ups! Esa no es una letra válida.')
                            
                        print(f'No tienes advertencias disponibles, pierdes un intento: {current_guess}')

            is_winner_found = is_word_guessed(secret_word, guessed_letters)
            print(spacer)

        else:
            unique_letters = len(set(secret_word))
            score = avail_guesses * unique_letters
            print('¡Felicidades, has ganado!! :D ')
            return f'Tu puntaje total para este juego es: {score}'
        
    update_drawing(drawing, avail_guesses)
    return f'Lo siento, te has quedado sin intentos. La palabra era "{secret_word}".'


def main():
    print("Cargando lista de palabras desde el archivo...")
    word_list = load_words()
    secret_word = random.choice(word_list)

    print(f"{len(word_list)} palabras cargadas.\n")

    ready_to_play = input("¿Estás listo para jugar? (Y o N): ")

    if ready_to_play.lower() in "Yy":
        print(hangman(secret_word))
    elif ready_to_play.lower() in "Nn":
        print("Hasta luego. ¡Gracias por jugar!")
    else:
        print("Opción no válida. Por favor, elige 'Y' para jugar o 'N' para salir.")

if __name__ == "__main__":
    main()
