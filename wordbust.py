# Muhammed Burhan's WordBust!

import pygame  # Import the pygame library for game development.
import sys  # Import the sys module for system-related functionality.
import random  # Import the random module for generating random numbers or selecting random elements.
from words import *  # Import the "words" module that contains a list of words for the game.

pygame.init()  # Initialize the pygame library and its modules.

# Game Window Dimensions
window_width, window_height = 633, 900

# Create the game window
game_window = pygame.display.set_mode((window_width, window_height))

# Load the background image
background_image = pygame.image.load("WordBustTiles.png")
background_rect = background_image.get_rect(center=(317, 300))

# Load the game icon
game_icon = pygame.image.load("bundesliga.png")

# Set the game window title and icon
pygame.display.set_caption("WordBust!")
pygame.display.set_icon(game_icon)


green = "#6aaa64"  # Color for correct letters in the guess
yellow = "#c9b458" # Color for incorrect letters in the guess
grey = "#787c7e"   # Color for empty/unused letters
outline_colour = "#d3d6da" # Color for letter outlines
filled_outline_colour = "#878a8c" # Color for filled letter outlines

# Randomly chosen word for the game from the words module
correct_word = random.choice(list_of_words)
# Define the alphabet layout
alphabet_layout = ["QWERTYUIOP", "ASDFGHJKL", "ZXCVBNM"]

# Set fonts for guessed letters and available letters
guessed_letter_font = pygame.font.Font("FreeSansBold.otf",60)
available_letter_font = pygame.font.Font("FreeSansBold.otf", 40)

# Clear the game window and display the background image
game_window.fill("#FFE4C4")
game_window.blit(background_image, background_rect)
pygame.display.update()

# Constants for letter spacing and size
letter_spacing_x = 85
letter_spacing_y = 12
size_of_letters = 75

# Global variables
guesses_count = 0

# guesses is a 2D list that will be storing the guesses. A guess will be a list of letters.
# The list will be iterated through and each letter in each guess will be drawn on the screen.
guesses = [[]] * 6

current_guess = []
current_guess_string = ""
current_letter_bg_x = 110

# The "indicators" list contains objects representing the buttons with letters, commonly referred to as indicators. 
# These indicators display the available letters for selection in the game.
indicators = []

# game_result stores the result of the game (Win or Loss).
game_result = ""


# Letter class represents a single letter object.
class Letter:
    def __init__(self, text, bg_position):
        # Initializes variables such as background color, text color, position, and size.
        self.bg_color = "white"
        self.text_color = "black"
        self.bg_position = bg_position
        self.bg_x = bg_position[0]
        self.bg_y = bg_position[1]
        self.bg_rect = (bg_position[0], self.bg_y, size_of_letters, size_of_letters)
        self.text = text
        self.text_position = (self.bg_x + 36, self.bg_position[1] + 34)
        self.text_surface = guessed_letter_font.render(self.text, True, self.text_color)
        self.text_rect = self.text_surface.get_rect(center=self.text_position)

    def draw(self):
        # Draws the letter and its text on the screen at the desired positions.
        pygame.draw.rect(game_window, self.bg_color, self.bg_rect)
        if self.bg_color == "white":
            pygame.draw.rect(game_window, filled_outline_colour, self.bg_rect, 3)
        self.text_surface = guessed_letter_font.render(self.text, True, self.text_color)
        game_window.blit(self.text_surface, self.text_rect)
        pygame.display.update()

    def delete(self):
        # Deletes the letter by filling its spot with a default square.
        pygame.draw.rect(game_window, "white", self.bg_rect)
        pygame.draw.rect(game_window, outline_colour, self.bg_rect, 3)
        pygame.display.update()

class Indicator:
    def __init__(self, x, y, letter):
        # Initializes variables such as position, size, and letter.
        self.x = x
        self.y = y
        self.text = letter
        self.rect = (self.x, self.y, 57, 75)
        self.bg_color = outline_colour

    def draw(self):
        # Draws the indicator and its text on the screen at the desired position.
        pygame.draw.rect(game_window, self.bg_color, self.rect)
        self.text_surface = available_letter_font.render(self.text, True, "black")
        self.text_rect = self.text_surface.get_rect(center=(self.x+27, self.y+30))
        game_window.blit(self.text_surface, self.text_rect)
        pygame.display.update()


# Drawing the indicators on the screen.
indicator_x, indicator_y =20, 600

for i in range(3):
    for letter in alphabet_layout[i]:
        new_indicator = Indicator(indicator_x, indicator_y, letter)
        indicators.append(new_indicator)
        new_indicator.draw()
        indicator_x += 60
    indicator_y += 100
    if i == 0:
        indicator_x = 50
    elif i == 1:
        indicator_x = 105

def check_guess(guess_to_check):
    # Checks each letter in the guess and updates its color based on correctness.
    global current_guess, current_guess_string, guesses_count, current_letter_bg_x, game_result
    game_decided = False
    for i in range(5):
        lowercase_letter = guess_to_check[i].text.lower()
        if lowercase_letter in correct_word:
            if lowercase_letter == correct_word[i]:
                guess_to_check[i].bg_color = green
                for indicator in indicators:
                    if indicator.text == lowercase_letter.upper():
                        indicator.bg_color = green
                        indicator.draw()
                guess_to_check[i].text_color = "white"
                if not game_decided:
                    game_result = "W"
            else:
                guess_to_check[i].bg_color = yellow
                for indicator in indicators:
                    if indicator.text == lowercase_letter.upper():
                        indicator.bg_color = yellow
                        indicator.draw()
                guess_to_check[i].text_color = "white"
                game_result = ""
                game_decided = True
        else:
            guess_to_check[i].bg_color = grey
            for indicator in indicators:
                if indicator.text == lowercase_letter.upper():
                    indicator.bg_color = grey
                    indicator.draw()
            guess_to_check[i].text_color = "white"
            game_result = ""
            game_decided = True
        guess_to_check[i].draw()
        pygame.display.update()
    
    guesses_count += 1
    current_guess = []
    current_guess_string = ""
    current_letter_bg_x = 110

    if guesses_count == 6 and game_result == "":
        game_result = "L"

def play_again():
    # Puts the play again text on the screen.
    pygame.draw.rect(game_window, "#FFE4C4", (10, 600, 1000, 600))
    play_again_font = pygame.font.Font("FreeSansBold.otf", 40)
    play_again_text = play_again_font.render("Press ENTER to Play Again!", True, "black")  # Render the play again text.
    play_again_rect = play_again_text.get_rect(center=(window_width/2, 700))  # Get the rectangle for centering the play again text
    word_was_text = play_again_font.render(f"The word was {correct_word}!", True, "black")
    word_was_rect = word_was_text.get_rect(center=(window_width/2, 650))
    game_window.blit(word_was_text, word_was_rect)
    game_window.blit(play_again_text, play_again_rect)
    pygame.display.update()

def reset():
    # Resets all global variables to their default states.
    global guesses_count, correct_word, guesses, current_guess, current_guess_string, game_result
    game_window.fill("#FFE4C4")
    game_window.blit(background_image, background_rect)
    guesses_count = 0
    correct_word = random.choice(list_of_words)
    guesses = [[]] * 6
    current_guess = []
    current_guess_string = ""
    game_result = ""
    pygame.display.update()
    for indicator in indicators:
        indicator.bg_color = outline_colour
        indicator.draw()

def create_new_letter():
    # Creates a new letter and adds it to the guess.
    global current_guess_string, current_letter_bg_x
    current_guess_string += key_pressed
    new_letter = Letter(key_pressed, (current_letter_bg_x, guesses_count * 100 + letter_spacing_y))
    current_letter_bg_x += letter_spacing_x
    guesses[guesses_count].append(new_letter)
    current_guess.append(new_letter)
    for guess in guesses:
        for letter in guess:
            letter.draw()

def delete_letter():
    # Deletes the last letter from the guess.
    global current_guess_string, current_letter_bg_x
    guesses[guesses_count][-1].delete()
    guesses[guesses_count].pop()
    current_guess_string = current_guess_string[:-1]
    current_guess.pop() 
    current_letter_bg_x -= letter_spacing_x

while True:
    if game_result != "":
        play_again()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                if game_result != "":
                    reset()
                else:
                    if len(current_guess_string) == 5 and current_guess_string.lower() in list_of_words:
                        check_guess(current_guess)
            elif event.key == pygame.K_BACKSPACE:
                if len(current_guess_string) > 0:
                    delete_letter()
            else:
                key_pressed = event.unicode.upper()
                if key_pressed in "QWERTYUIOPASDFGHJKLZXCVBNM" and key_pressed != "":
                    if len(current_guess_string) < 5:
                        create_new_letter()