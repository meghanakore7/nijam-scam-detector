"""
try_it.py
---------
A small interactive script so you (or anyone reviewing this project) can
type in any message and immediately see Nijam's verdict and reasoning,
without needing to know the command line syntax.

Usage:
    python try_it.py
"""

from nijam.classifier import load_model
from nijam.detector import analyze_message, print_report


def main():
    print("Nijam — Scam Message Detector")
    print("Type a message to check it, or 'quit' to exit.\n")

    model = load_model()

    while True:
        text = input("Message > ").strip()
        if text.lower() in {"quit", "exit"}:
            break
        if not text:
            continue
        result = analyze_message(text, model=model)
        print_report(text, result)
        print()


if __name__ == "__main__":
    main()
