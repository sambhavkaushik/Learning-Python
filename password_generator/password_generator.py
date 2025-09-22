# Password Generator (Beginner-friendly, Secure)
# - Uses Python's 'secrets' for strong randomness
# - Lets you choose length, how many passwords, and character types
# - Ensures at least one char from each chosen category

import secrets
import string

AMBIGUOUS = set("O0oIl1|`'\";:,.(){}[]<>")

def ask_yes_no(prompt: str, default: bool) -> bool:
    d = "Y/n" if default else "y/N"
    while True:
        ans = input(f"{prompt} ({d}): ").strip().lower()
        if not ans:
            return default
        if ans in ("y", "yes"):
            return True
        if ans in ("n", "no"):
            return False
        print("Please answer with y/n.")

def ask_int(prompt: str, default: int, min_val: int = 1, max_val: int = 200) -> int:
    while True:
        raw = input(f"{prompt} [default {default}]: ").strip()
        if not raw:
            return default
        if raw.isdigit():
            val = int(raw)
            if min_val <= val <= max_val:
                return val
        print(f"Enter a number between {min_val} and {max_val}.")

def build_pool(use_lower: bool, use_upper: bool, use_digits: bool, use_symbols: bool, avoid_ambiguous: bool):
    pools = []
    if use_lower:
        pools.append(set(string.ascii_lowercase))
    if use_upper:
        pools.append(set(string.ascii_uppercase))
    if use_digits:
        pools.append(set(string.digits))
    if use_symbols:
        # Safe subset of punctuation
        pools.append(set("!@#$%^&*_-+=?~"))

    if not pools:
        pools = [set(string.ascii_lowercase), set(string.digits)]

    if avoid_ambiguous:
        pools = [s - AMBIGUOUS for s in pools]

    combined = set().union(*pools)
    return pools, list(combined)

def generate_password(length: int, pools, combined_pool) -> str:
    if len(combined_pool) == 0:
        raise ValueError("Character pool is empty. Try enabling more character types.")

    password_chars = []

    # Ensure at least one char from each selected pool
    for s in pools:
        if s:
            password_chars.append(secrets.choice(list(s)))

    if len(password_chars) > length:
        length = len(password_chars)

    # Fill the rest
    remaining = length - len(password_chars)
    for _ in range(remaining):
        password_chars.append(secrets.choice(combined_pool))

    # Shuffle
    for i in range(len(password_chars) - 1, 0, -1):
        j = secrets.randbelow(i + 1)
        password_chars[i], password_chars[j] = password_chars[j], password_chars[i]

    return "".join(password_chars)

def main():
    print("=== Password Generator ===")
    length = ask_int("Password length", default=12, min_val=4, max_val=128)
    count  = ask_int("How many passwords to generate", default=3, min_val=1, max_val=20)

    use_lower = ask_yes_no("Include lowercase letters?", True)
    use_upper = ask_yes_no("Include uppercase letters?", True)
    use_digits = ask_yes_no("Include digits?", True)
    use_symbols = ask_yes_no("Include symbols?", True)
    avoid_amb = ask_yes_no("Avoid ambiguous characters (O/0, l/1, etc.)?", True)

    pools, combined_pool = build_pool(use_lower, use_upper, use_digits, use_symbols, avoid_amb)

    print("\nGenerated Passwords:")
    print("-" * 30)
    for _ in range(count):
        pw = generate_password(length, pools, combined_pool)
        print(pw)
    print("-" * 30)

if __name__ == "__main__":
    main()
