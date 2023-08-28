# Anki Decks Migration/Transfer

This script is designed to assist in transferring learning records from one deck to another.

For instance, suppose you have two identical cards (with word spellings as the basis for comparison) in Deck A and Deck B. You've been using Deck A for three months, but you've found a better deck with no learning records. This script will help you "sync" the learning records for these identical cards.

## Prerequisites

- Anki Add-on: Anki-Connect installed
- Python Environment with urllib installed

## Usage

**Please back up the target deck before proceeding.**

To get started, follow these steps:

1. Edit the following lines at the beginning of the script:

```python
url = 'http://127.0.0.1:8765' # Anki Connect URL
origin_deck = "xxx"          # Source deck name
target_deck = "xxx"          # Target deck name
origin_word_field_name = "xx"  # Field name in the source deck
target_word_field_name = "xx"  # Field name in the target deck
```

Replace the placeholders with the appropriate values.

2. Run the script.

3. You're done! Your learning records should now be synchronized.

Enjoy your improved deck!



