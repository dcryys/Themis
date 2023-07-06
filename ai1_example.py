#!/usr/bin/env python3
import ai1

# Example usage
question = "Give me recipe of draniki"
print("Asking:", question)
answer = ai1.ask_gpt3(question)
print(f"Q: {question}\nA: {answer}")
