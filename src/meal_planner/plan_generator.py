import os
import yaml # For loading the prompt from YAML
import json # For potentially validating/handling JSON

# Import functions from our other modules within the same package
from .llm_client import generate_text_with_retry, parse_json_output, GENERATION_CONFIG_JSON
from .user_input import load_user_profile

def load_prompt_template(file_path, prompt_key):
    """Loads a specific prompt template from a YAML file."""
    try:
        if not os.path.exists(file_path):
            print(f"Error: Prompt template file not found at {file_path}")
            return None
        with open(file_path, 'r', encoding='utf-8') as f:
            prompts = yaml.safe_load(f)
        # Assuming the key for the basic plan prompt is prompt key
        template = prompts.get(prompt_key)
        if not template:
            print(f"Error: Key '{prompt_key}' not found in {file_path}")
            return None
        print(f"Successfully loaded prompt template from: {file_path}")
        return template
    except yaml.YAMLError as e:
        print(f"Error parsing YAML file {file_path}: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred loading prompt template: {e}")
        return None

def format_prompt(template, user_profile):
    """Formats the prompt template with user profile data."""
    try:
        # Prepare data for formatting, handling potentially missing keys gracefully
        profile_data = {
            "fitness_goal": user_profile.get("fitness_goal", "Not specified"),
            "dietary_preferences": ", ".join(user_profile.get("dietary_preferences", [])),
            "allergies_or_avoidances": ", ".join(user_profile.get("allergies_or_avoidances", [])),
            "taste_preferences": ", ".join(user_profile.get("taste_preferences", [])),
            "schedule_constraints": ", ".join(user_profile.get("schedule_constraints", [])),
            "specific_requests": ", ".join(user_profile.get("specific_requests", []))
        }
        # Use the format method to insert data into placeholders like {fitness_goal}
        formatted = template.format(**profile_data)
        return formatted
    except KeyError as e:
        print(f"Error: Missing key in user profile needed for prompt formatting: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred during prompt formatting: {e}")
        return None

def generate_basic_plan(user_profile_path, prompt_template_path):
    """
    Generates a basic 7-day meal plan JSON based on user profile and prompt template.

    Args:
        user_profile_path (str): Path to the user profile JSON file.
        prompt_template_path (str): Path to the prompt template YAML file.

    Returns:
        dict: The parsed meal plan as a dictionary, or None if generation fails.
    """
    print("--- Starting Basic Meal Plan Generation ---")

    # 1. Load User Profile
    print(f"Loading user profile from: {user_profile_path}")
    user_profile = load_user_profile(user_profile_path)
    if not user_profile:
        print("Failed to load user profile. Aborting.")
        return None

    # 2. Load Prompt Template
    print(f"Loading prompt template from: {prompt_template_path}")
    prompt_template = load_prompt_template(prompt_template_path, 'basic_meal_plan_prompt')
    if not prompt_template:
        print("Failed to load prompt template. Aborting.")
        return None

    # 3. Format Prompt
    print("Formatting prompt with user data...")
    formatted_prompt = format_prompt(prompt_template, user_profile)
    if not formatted_prompt:
        print("Failed to format prompt. Aborting.")
        return None
    # print(f"\n--- Formatted Prompt (First 500 chars) ---\n{formatted_prompt[:500]}...\n-----------------------------------\n") # Optional: Debug print

    # 4. Call LLM API (Requesting JSON output via config)
    print("Calling LLM to generate meal plan...")
    # Use the specific config designed for JSON output
    raw_llm_output = generate_text_with_retry(
        prompt_text=formatted_prompt,
        generation_config=GENERATION_CONFIG_JSON # Pass the JSON config
    )

    if not raw_llm_output:
        print("LLM generation failed or returned empty response. Aborting.")
        return None

    # 5. Parse JSON Output
    print("Parsing LLM response as JSON...")
    parsed_plan = parse_json_output(raw_llm_output)

    if not parsed_plan:
        print("Failed to parse LLM output as JSON. Aborting.")
        return None

    print("--- Basic Meal Plan Generation Successful ---")
    return parsed_plan


def generate_detailed_plan(user_profile_path, prompt_template_path):
        """
        Generates a DETAILED 7-day meal plan JSON including recipes, ingredients, times.

        Args:
            user_profile_path (str): Path to the user profile JSON file.
            prompt_template_path (str): Path to the prompt template YAML file.

        Returns:
            dict: The parsed detailed meal plan as a dictionary, or None if generation fails.
        """
        print("--- Starting Detailed Meal Plan Generation ---")

        # 1. Load User Profile
        print(f"Loading user profile from: {user_profile_path}")
        user_profile = load_user_profile(user_profile_path)
        if not user_profile:
            print("Failed to load user profile. Aborting.")
            return None

        # 2. Load DETAILED Prompt Template
        print(f"Loading DETAILED prompt template from: {prompt_template_path}")
        # Load the specific key for the detailed prompt
        prompt_template = load_prompt_template(prompt_template_path, 'detailed_meal_plan_prompt')
        if not prompt_template:
            print("Failed to load detailed prompt template. Aborting.")
            return None

        # 3. Format Prompt
        print("Formatting detailed prompt with user data...")
        formatted_prompt = format_prompt(prompt_template, user_profile)
        if not formatted_prompt:
            print("Failed to format detailed prompt. Aborting.")
            return None
        # print(f"\n--- Formatted Detailed Prompt (First 500 chars) ---\n{formatted_prompt[:500]}...\n-----------------------------------\n") # Optional: Debug print

        # 4. Call LLM API (Still requesting JSON output via config)
        print("Calling LLM to generate DETAILED meal plan...")
        # Use the same JSON config, as we still want JSON output
        raw_llm_output = generate_text_with_retry(
            prompt_text=formatted_prompt,
            generation_config=GENERATION_CONFIG_JSON
        )

        if not raw_llm_output:
            print("LLM generation failed or returned empty response for detailed plan. Aborting.")
            return None

        # 5. Parse JSON Output
        print("Parsing detailed LLM response as JSON...")
        # Use the same JSON parser
        parsed_plan = parse_json_output(raw_llm_output)

        if not parsed_plan:
            print("Failed to parse detailed LLM output as JSON. Aborting.")
            return None

        # Optional: Add validation against the detailed schema here later if needed

        print("--- Detailed Meal Plan Generation Successful ---")
        return parsed_plan





# Example Usage (Optional - for testing this file directly)
if __name__ == '__main__':
    print("Testing Plan Generator...")
    # Construct paths relative to the project root assuming this script
    # might be run from the root for testing.
    # Adjust if running directly from src/meal_planner
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    test_profile_path = os.path.join(project_root, 'data', 'examples', 'user_profile_1.json')
    test_prompt_path = os.path.join(project_root, 'config', 'prompts.yaml')

    print(f"Using profile: {test_profile_path}")
    print(f"Using prompt: {test_prompt_path}")

    # Check if files exist before running
    if not os.path.exists(test_profile_path):
         print(f"ERROR: Test profile not found at {test_profile_path}")
    elif not os.path.exists(test_prompt_path):
         print(f"ERROR: Test prompt file not found at {test_prompt_path}")
    else:
        generated_plan = generate_detailed_plan(test_profile_path, test_prompt_path)

        if generated_plan:
            print("\n--- Generated Plan (Output) ---")
            # Pretty print the resulting dictionary
            print(json.dumps(generated_plan, indent=4))
        else:
            print("\n--- Plan Generation Failed ---")