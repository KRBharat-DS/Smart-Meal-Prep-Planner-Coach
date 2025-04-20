import json
import os # Import os to construct paths reliably


def load_user_profile(file_path):
    """
    Loads user profile data from a JSON file.

    Args:
        file_path (str): The path to the JSON file containing user profile data.

    Returns:
        dict: A dictionary containing the user profile data,
              or None if an error occurs (e.g., file not found, invalid JSON).
    """
    try:
        # Ensure the file path exists
        if not os.path.exists(file_path):
            print(f"Error: File not found at {file_path}")
            return None

        with open(file_path, 'r', encoding='utf-8') as f:
            user_profile = json.load(f)
        print(f"Successfully loaded user profile from: {file_path}")
        return user_profile
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in file: {file_path}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred while loading {file_path}: {e}")
        return None

# Example of how you might use this function (optional, for testing within the file)
if __name__ == '__main__':
    # This part only runs when you execute this script directly (python user_input.py)
    # It assumes you run it from the project root directory
    example_path = os.path.join('data', 'examples', 'user_profile_1.json')
    profile = load_user_profile(example_path)
    if profile:
        print("\n--- Example Profile Data ---")
        print(profile)
        print(f"\nFitness Goal: {profile.get('fitness_goal', 'Not specified')}")