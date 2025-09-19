import random

# Generate a random integer between 1 and 100 (inclusive)
num = random.randint(1, 100)
print("Welcome to the Number Guessing Game!")
print("I have selected a number between 1 and 100.")
print("You have 10 attempts to guess the number.")
attempts = 10
while attempts > 0:
    guess = input(f"You have {attempts} attempts left. Enter your guess: ")
    try: # Validate input
        guess = int(guess)
        if guess < 1 or guess > 100:
            print("Please enter a number between 1 and 100.")
            continue
    except ValueError:
        print("Invalid input. Please enter a valid integer between 1 and 100.")
        continue
    # Check the guess
    if guess < num:
        print("Too low!")
    elif guess > num:
        print("Too high!")
    else:
        print(f"Congratulations! You've guessed the number {num} correctly!")
        break
    attempts -= 1
