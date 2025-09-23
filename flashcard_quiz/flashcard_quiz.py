# Flashcards Quiz App (Console)
# - Stores flashcards in flashcards.json (auto-created with sample data)
# - Quiz mode (randomized), add/list/delete cards, per-card stats
# - Beginner-friendly, no external libraries

import json
import os
import random
from typing import List, Dict

DATA_FILE = "flashcards.json"

# -----------------------------
# Data helpers
# -----------------------------
def load_cards() -> List[Dict]:
    if not os.path.exists(DATA_FILE):
        # Seed with sample cards on first run
        sample = [
            {"q": "Capital of France?", "a": "Paris", "correct": 0, "attempts": 0},
            {"q": "2 + 2 = ?", "a": "4", "correct": 0, "attempts": 0},
            {"q": "Python list to get length?", "a": "len", "correct": 0, "attempts": 0},
            {"q": "HTTP stands for?", "a": "HyperText Transfer Protocol|hypertext transfer protocol", "correct": 0, "attempts": 0},
        ]
        save_cards(sample)
        return sample
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_cards(cards: List[Dict]) -> None:
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(cards, f, ensure_ascii=False, indent=2)

# -----------------------------
# Utility
# -----------------------------
def normalize(s: str) -> str:
    return s.strip().lower()

def is_correct(user_ans: str, correct_field: str) -> bool:
    # Allow multiple answers separated by '|'
    answers = [normalize(x) for x in correct_field.split("|")]
    return normalize(user_ans) in answers

def pause():
    input("\nPress ENTER to continue...")

# -----------------------------
# Features
# -----------------------------
def quiz_mode(cards: List[Dict]) -> None:
    if not cards:
        print("No flashcards yet. Add some first.")
        return

    print("\n=== QUIZ MODE ===")
    print("Type 'q' to quit quiz mode.\n")
    order = cards[:]  # shallow copy
    random.shuffle(order)

    total = 0
    correct = 0

    for card in order:
        print(f"Q: {card['q']}")
        ans = input("Your answer: ").strip()
        if ans.lower() == "q":
            break
        card["attempts"] = card.get("attempts", 0) + 1
        total += 1
        if is_correct(ans, card["a"]):
            print("✅ Correct!")
            card["correct"] = card.get("correct", 0) + 1
            correct += 1
        else:
            print(f"❌ Incorrect. Correct answer: {card['a']}")
        print()

    save_cards(cards)
    if total > 0:
        print(f"Score: {correct}/{total} ({round(correct/total*100, 1)}%)")
    else:
        print("No questions answered.")

def add_card(cards: List[Dict]) -> None:
    print("\n=== ADD FLASHCARD ===")
    q = input("Enter question: ").strip()
    if not q:
        print("Question cannot be empty.")
        return
    a = input("Enter answer (use '|' for multiple valid answers): ").strip()
    if not a:
        print("Answer cannot be empty.")
        return
    cards.append({"q": q, "a": a, "correct": 0, "attempts": 0})
    save_cards(cards)
    print("✅ Flashcard added.")

def list_cards(cards: List[Dict]) -> None:
    print("\n=== FLASHCARDS ===")
    if not cards:
        print("(empty)")
        return
    for i, c in enumerate(cards, 1):
        acc = f"{c.get('correct',0)}/{c.get('attempts',0)}"
        print(f"{i}. Q: {c['q']} | A: {c['a']} | Stats: {acc}")

def delete_card(cards: List[Dict]) -> None:
    list_cards(cards)
    if not cards:
        return
    try:
        idx = int(input("\nEnter number to delete (0 to cancel): "))
    except ValueError:
        print("Please enter a valid number.")
        return
    if idx == 0:
        print("Canceled.")
        return
    if 1 <= idx <= len(cards):
        removed = cards.pop(idx - 1)
        save_cards(cards)
        print(f"🗑️ Deleted: {removed['q']}")
    else:
        print("Invalid index.")

def reset_stats(cards: List[Dict]) -> None:
    for c in cards:
        c["correct"] = 0
        c["attempts"] = 0
    save_cards(cards)
    print("🔄 Stats reset for all cards.")

# -----------------------------
# Menu
# -----------------------------
def menu():
    cards = load_cards()
    while True:
        print("\n=== Flashcards Quiz App ===")
        print("1) Quiz")
        print("2) Add flashcard")
        print("3) List flashcards")
        print("4) Delete flashcard")
        print("5) Reset stats")
        print("6) Exit")

        choice = input("Choose an option (1-6): ").strip()
        if choice == "1":
            quiz_mode(cards)
            pause()
        elif choice == "2":
            add_card(cards)
            pause()
        elif choice == "3":
            list_cards(cards)
            pause()
        elif choice == "4":
            delete_card(cards)
            pause()
        elif choice == "5":
            reset_stats(cards)
            pause()
        elif choice == "6":
            print("Bye! 👋")
            break
        else:
            print("Please choose a valid option (1-6).")

if __name__ == "__main__":
    menu()
