import json
from config import *

class HighScoreManager:
    """Manages loading and saving the high score to a JSON file."""

    def __init__(self, file_name='high_score.json'):
        """Initialize the high score manager with a specified file name."""
        self.file_name = file_name

    def load_high_score(self):
        """
        Load the high score from the JSON file.
        
        Returns:
            int: The high score if available, otherwise 0.
        """
        try:
            with open(self.file_name, 'r') as f:
                data = json.load(f)
                return data.get('high_score', 0)
        except (FileNotFoundError, json.JSONDecodeError):
            # Return 0 if file doesn't exist or has invalid format
            return 0

    def save_high_score(self, score):
        """
        Save the high score to the JSON file if the new score is greater.

        Args:
            score (int): The score to save if it's a new high score.
        """
        try:
            high_score = self.load_high_score()
            if score > high_score:
                with open(self.file_name, 'w') as f:
                    json.dump({'high_score': score}, f)
        except Exception as e:
            # Log the error without halting the program
            print(f"Error saving high score: {e}")
