# Вордл (Russian Wordle)

A terminal-based Wordle clone in Russian. Guess the hidden 5-letter Russian word in 6 tries.

## How to play

```bash
python3 wordle.py
```

- Each guess must be exactly 5 Russian letters.
- After each guess, tiles show how close you were:
  - **Green** — correct letter, correct position
  - **Yellow** — correct letter, wrong position
  - **Gray** — letter not in the word
- A new word is selected each day (seeded by today's date).

## Requirements

Python 3.6+ — no external dependencies.
