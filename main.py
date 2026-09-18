import os
import random
import time


def play_tone_sequence(notes):
    for frequency, duration in notes:
        try:
            import winsound

            winsound.Beep(int(frequency), int(duration * 1000))
        except ImportError:
            print("\a", end="", flush=True)
            time.sleep(duration)


def play_jeopardy_intro():
    melody = [
        (392, 0.18),
        (523.25, 0.18),
        (659.25, 0.18),
        (783.99, 0.18),
        (659.25, 0.22),
        (523.25, 0.22),
        (392, 0.3),
    ]
    play_tone_sequence(melody)


def play_success_sound():
    play_tone_sequence([(659.25, 0.1), (783.99, 0.1), (1046.5, 0.2)])


def play_error_sound():
    play_tone_sequence([(220, 0.08), (180, 0.08)])


def choose_difficulty():
    while True:
        print("\nChoose difficulty:")
        print("1. Easy")
        print("2. Normal")
        print("3. Hard")
        print("4. Quit")

        choice = input("Select an option (1-4): ").strip().lower()

        if choice in ("1", "easy"):
            return {"min": 1, "max": 20, "tries": 10, "time": 120}
        if choice in ("2", "normal"):
            return {"min": 1, "max": 50, "tries": 8, "time": 90}
        if choice in ("3", "hard"):
            return {"min": 1, "max": 100, "tries": 6, "time": 60}
        if choice in ("4", "done", "quit", "exit"):
            print("GG's Bru, Thanks for playing anyways!")
            raise SystemExit

        print("Invalid choice. Please choose 1, 2, 3, or 4.")


def play_game():
    difficulty = choose_difficulty()
    min_value = difficulty["min"]
    max_value = difficulty["max"]
    max_attempts = difficulty["tries"]
    timer_seconds = difficulty["time"]
    secret_number = random.randint(min_value, max_value)
    attempts = 0
    start_time = time.monotonic()

    print("Welcome to the First Game of the Day!")
    play_jeopardy_intro()
    print(f"I picked a number between {min_value} and {max_value}.")
    print(f"You have {max_attempts} chances and {timer_seconds} seconds to win!")

    while attempts < max_attempts:
        elapsed = time.monotonic() - start_time
        remaining = max(0, timer_seconds - int(elapsed))

        if remaining <= 0:
            print(f"Time's up! The number was {secret_number}.")
            play_error_sound()
            return

        minutes, seconds = divmod(remaining, 60)
        print(f"Time left: {minutes:02d}:{seconds:02d}")

        try:
            guess = int(input("Enter your guess: "))
        except ValueError:
            print("Please enter a valid number.")
            play_error_sound()
            continue
        except EOFError:
            print("\nInput closed. Bye!")
            return

        attempts += 1

        if guess < secret_number:
            print("Too Minimum! Try again.")
            play_error_sound()
        elif guess > secret_number:
            print("Too Peak! Try again.")
            play_error_sound()
        else:
            print(f"Correct! You guessed the number in {attempts} tries!")
            play_success_sound()
            return

    print(f"Game over! The number was {secret_number}.")
    play_error_sound()


if __name__ == "__main__":
    play_game()
