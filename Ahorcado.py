import random
import requests
import os
import time
from colorama import init, Fore, Style

init()

class HangmanGame:
    def __init__(self):
        self.words_api_key = None  
        self.categories = {
            1: "animal",
            2: "food",
            3: "sports",
            4: "countries",
            5: "professions"
        }
        self.difficulty_levels = {
            1: {"name": "Fácil", "max_errors": 8},
            2: {"name": "Medio", "max_errors": 6},
            3: {"name": "Difícil", "max_errors": 4}
        }
        self.hangman_stages = [
            '''
               --------
               |      |
               |      
               |    
               |      
               |     
               -
            ''',
            '''
               --------
               |      |
               |      O
               |    
               |      
               |     
               -
            ''',
            '''
               --------
               |      |
               |      O
               |      |
               |      
               |     
               -
            ''',
            '''
               --------
               |      |
               |      O
               |     /|
               |      
               |     
               -
            ''',
            '''
               --------
               |      |
               |      O
               |     /|\\
               |      
               |     
               -
            ''',
            '''
               --------
               |      |
               |      O
               |     /|\\
               |     /
               |     
               -
            ''',
            '''
               --------
               |      |
               |      O
               |     /|\\
               |     / \\
               |     
               -
            '''
        ]
        self.score = 0
        self.words_cache = {}

    def get_random_word(self, category):
        if not self.words_api_key:
            backup_words = {
                "animal": ["perro", "gato", "elefante", "jirafa", "leon"],
                "food": ["pizza", "hamburguesa", "pasta", "tacos", "sushi"],
                "sports": ["futbol", "tenis", "baloncesto", "natacion", "voleibol"],
                "countries": ["mexico", "españa", "francia", "brasil", "japon"],
                "professions": ["doctor", "profesor", "ingeniero", "chef", "arquitecto"]
            }
            return random.choice(backup_words.get(category, backup_words["animal"]))

        # Cache check
        if category in self.words_cache:
            return random.choice(self.words_cache[category])

        try:
            url = f"https://wordsapiv1.p.rapidapi.com/words/"
            headers = {
                "X-RapidAPI-Key": self.words_api_key,
                "X-RapidAPI-Host": "wordsapiv1.p.rapidapi.com"
            }
            params = {
                "partOfSpeech": "noun",
                "topics": category
            }
            response = requests.get(url, headers=headers, params=params)
            if response.status_code == 200:
                words = response.json().get("words", [])
                self.words_cache[category] = words
                return random.choice(words)
        except:
            pass
        
        backup_words = ["python", "programacion", "computadora", "tecnologia"]
        return random.choice(backup_words)

    def display_menu(self, options, title):
        print(f"\n{Fore.CYAN}{title}{Style.RESET_ALL}")
        for key, value in options.items():
            if isinstance(value, dict):
                print(f"{key}. {value['name']}")
            else:
                print(f"{key}. {value}")
        while True:
            try:
                choice = input("\nSelecciona una opción: ")
                if not choice.isdigit():
                    print(f"{Fore.RED}Por favor, ingresa un número.{Style.RESET_ALL}")
                    continue
                choice = int(choice)
                if choice not in options:
                    print(f"{Fore.RED}Opción no válida. Elige un número entre {min(options.keys())} y {max(options.keys())}{Style.RESET_ALL}")
                    continue
                return choice
            except ValueError:
                print(f"{Fore.RED}Por favor, ingresa un número válido.{Style.RESET_ALL}")

    def play_game(self):
        while True:
            os.system('cls' if os.name == 'nt' else 'clear')
            print(f"{Fore.GREEN}=== JUEGO DEL AHORCADO ==={Style.RESET_ALL}")
            print(f"Puntaje actual: {self.score}")

            category_choice = self.display_menu(self.categories, "Categorías disponibles:")
            category = self.categories.get(category_choice)

            difficulty_choice = self.display_menu(self.difficulty_levels, "Niveles de dificultad:")
            difficulty = self.difficulty_levels.get(difficulty_choice)

            if not category or not difficulty:
                print("Opción inválida")
                continue

            word = self.get_random_word(category).lower()
            guessed_letters = set()
            errors = 0
            max_errors = difficulty["max_errors"]

            while errors < max_errors:
                os.system('cls' if os.name == 'nt' else 'clear')
                print(f"\n{Fore.YELLOW}Categoría: {category.title()}{Style.RESET_ALL}")
                print(f"{Fore.YELLOW}Nivel: {difficulty['name']}{Style.RESET_ALL}")
                print(f"Errores permitidos: {max_errors - errors}")
                print(self.hangman_stages[min(errors, len(self.hangman_stages)-1)])

                display = ""
                for letter in word:
                    if letter.isalpha():
                        if letter in guessed_letters:
                            display += letter + " "
                        else:
                            display += "_ "
                    else:
                        display += letter + " "
                print(f"\nPalabra: {display}")
                print("\nLetras usadas:", " ".join(sorted(guessed_letters)))

                if all(letter in guessed_letters or not letter.isalpha() for letter in word):
                    print(f"\n{Fore.GREEN}¡Felicidades! Has ganado. La palabra era: {word}{Style.RESET_ALL}")
                    self.score += (max_errors - errors) * difficulty_choice
                    break

                guess = input("\nIngresa una letra: ").lower()
                
                # Validación de entrada
                if not guess:
                    print(f"{Fore.RED}Por favor, ingresa una letra.{Style.RESET_ALL}")
                    time.sleep(1)
                    continue
                
                if len(guess) > 1:
                    print(f"{Fore.RED}Por favor, ingresa solo una letra.{Style.RESET_ALL}")
                    time.sleep(1)
                    continue

                if not guess.isalpha():
                    print(f"{Fore.RED}Por favor, ingresa solo letras (no números ni símbolos).{Style.RESET_ALL}")
                    time.sleep(1)
                    continue

                if guess in guessed_letters:
                    print(f"{Fore.YELLOW}Ya has intentado esa letra. Prueba con otra.{Style.RESET_ALL}")
                    time.sleep(1)
                    continue

                guessed_letters.add(guess)
                if guess not in word:
                    errors += 1
                    if errors >= max_errors:
                        os.system('cls' if os.name == 'nt' else 'clear')
                        print(self.hangman_stages[-1])
                        print(f"\n{Fore.RED}¡Game Over! La palabra era: {word}{Style.RESET_ALL}")

            while True:
                play_again = input("\n¿Quieres jugar otra vez? (s/n): ").lower()
                if play_again in ['s', 'n']:
                    break
                print(f"{Fore.RED}Por favor, ingresa 's' para sí o 'n' para no.{Style.RESET_ALL}")
            if play_again != 's':
                print(f"\n{Fore.CYAN}Puntaje final: {self.score}{Style.RESET_ALL}")
                print("¡Gracias por jugar!")
                break

if __name__ == "__main__":
    game = HangmanGame()
    game.play_game()