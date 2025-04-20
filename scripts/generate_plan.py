import os
import sys
import json
import argparse # Library for handling command-line arguments

# --- Path Setup ---
# Get the absolute path to the project's root directory
# This assumes the script is in the 'scripts' folder, so we go up one level.

# --- Path Setup ---
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
SRC_PATH = os.path.join(PROJECT_ROOT, 'src')
if SRC_PATH not in sys.path:
    sys.path.insert(0, SRC_PATH)
    print(f"Added '{SRC_PATH}' to sys.path") # This line printed successfully

# --- Import Core Logic ---
print("DEBUG: Attempting to import core logic...") # ADDED
try:
    from meal_planner.plan_generator import generate_basic_plan, generate_detailed_plan
    print("DEBUG: Core logic imported successfully.") # ADDED
except ImportError as e:
    print(f"Error: Failed to import meal_planner module. Ensure '{SRC_PATH}' is correct and contains 'meal_planner'.")
    print(f"ImportError: {e}")
    print("DEBUG: Exiting due to import error.") # ADDED
    sys.exit(1)

# --- Default File Paths ---
# (Keep these as they are)
DEFAULT_PROFILE_DIR = os.path.join(PROJECT_ROOT, 'data', 'examples')
DEFAULT_PROMPT_PATH = os.path.join(PROJECT_ROOT, 'config', 'prompts.yaml')
DEFAULT_OUTPUT_DIR = os.path.join(PROJECT_ROOT, 'output')


# --- Main Execution Function ---
def main():
    print("DEBUG: Starting main function...") # ADDED
    # --- Argument Parsing ---
    parser = argparse.ArgumentParser(description="Generate a personalized 7-day meal plan using Generative AI.")
    # (Keep all parser.add_argument calls as they are)
    parser.add_argument("--profile", "-p", type=str, default=os.path.join(os.path.relpath(DEFAULT_PROFILE_DIR, PROJECT_ROOT), 'user_profile_1.json'), help=f"Path to the user profile JSON file (relative to project root). Default: data/examples/user_profile_1.json")
    parser.add_argument("--prompt", type=str, default=os.path.relpath(DEFAULT_PROMPT_PATH, PROJECT_ROOT), help=f"Path to the prompt template YAML file (relative to project root). Default: config/prompts.yaml")
    parser.add_argument("--output", "-o", type=str, default=os.path.join(os.path.relpath(DEFAULT_OUTPUT_DIR, PROJECT_ROOT), 'generated_plan.json'), help=f"Path to save the generated meal plan JSON file (relative to project root). Default: output/generated_plan.json")
    parser.add_argument("--detailed", action="store_true", help="Generate a detailed plan including recipes, ingredients, and times. Default is basic plan.")

    print("DEBUG: Parsing arguments...") # ADDED
    args = parser.parse_args()
    print(f"DEBUG: Arguments parsed: {args}") # ADDED

    # --- Resolve Paths Relative to PROJECT_ROOT ---
    print("DEBUG: Resolving paths...") # ADDED
    profile_file_path = os.path.abspath(os.path.join(PROJECT_ROOT, args.profile))
    prompt_file_path = os.path.abspath(os.path.join(PROJECT_ROOT, args.prompt))
    output_file_path = os.path.abspath(os.path.join(PROJECT_ROOT, args.output))
    print(f"DEBUG: Resolved Profile Path: {profile_file_path}") # ADDED
    print(f"DEBUG: Resolved Prompt Path: {prompt_file_path}") # ADDED
    print(f"DEBUG: Resolved Output Path: {output_file_path}") # ADDED

    # --- Input Validation (using resolved absolute paths) ---
    print("DEBUG: Checking profile existence...") # ADDED
    if not os.path.exists(profile_file_path):
        print(f"Error: User profile file not found at '{profile_file_path}'")
        print("DEBUG: Exiting due to missing profile file.") # ADDED
        sys.exit(1)
    print("DEBUG: Profile exists.") # ADDED

    print("DEBUG: Checking prompt existence...") # ADDED
    if not os.path.exists(prompt_file_path):
        print(f"Error: Prompt template file not found at '{prompt_file_path}'")
        print("DEBUG: Exiting due to missing prompt file.") # ADDED
        sys.exit(1)
    print("DEBUG: Prompt exists.") # ADDED

    # Ensure output directory exists (using resolved absolute path)
    print("DEBUG: Checking output directory...") # ADDED
    output_dir = os.path.dirname(output_file_path)
    if not os.path.exists(output_dir):
        print(f"Output directory '{output_dir}' not found. Creating it...")
        try:
            os.makedirs(output_dir)
            print(f"DEBUG: Created output directory: {output_dir}") # ADDED
        except OSError as e:
            print(f"Error: Could not create output directory '{output_dir}'. {e}")
            print("DEBUG: Exiting due to makedirs error.") # ADDED
            sys.exit(1)
    else:
        print("DEBUG: Output directory already exists.") # ADDED

    # --- Print Configuration ---
    print("--- Configuration ---") # This is the first non-debug print inside main
    print(f"User Profile: {profile_file_path}")
    print(f"Prompt Template: {prompt_file_path}")
    print(f"Output File: {output_file_path}")
    print("--------------------")

    # --- Generate Plan (using resolved absolute paths) ---
    if args.detailed:
        print("Generating DETAILED meal plan...")
        meal_plan_dict = generate_detailed_plan(
            user_profile_path=profile_file_path, # Use resolved path
            prompt_template_path=prompt_file_path # Use resolved path
        )
    else:
        print("Generating BASIC meal plan...")
        meal_plan_dict = generate_basic_plan(
            user_profile_path=profile_file_path, # Use resolved path
            prompt_template_path=prompt_file_path # Use resolved path
        )

    # --- Save Output (using resolved absolute path) ---
    if meal_plan_dict:
        print(f"\nSuccessfully generated meal plan. Saving to '{output_file_path}'...")
        try:
            # Use the resolved absolute output path for saving
            with open(output_file_path, 'w', encoding='utf-8') as f:
                json.dump(meal_plan_dict, f, indent=4, ensure_ascii=False)
            print("Meal plan saved successfully.")
        except IOError as e:
            print(f"Error: Could not write meal plan to file '{output_file_path}'. {e}")
            sys.exit(1)
        except Exception as e:
            print(f"An unexpected error occurred while saving the file: {e}")
            sys.exit(1)
    else:
        print("\nMeal plan generation failed. No output file created.")
        sys.exit(1) # Exit with error status if generation failed


# --- Script Entry Point ---
print("DEBUG: Checking if script is run directly...") # ADDED
if __name__ == "__main__":
    print("DEBUG: Running main()...") # ADDED
    main()
else:
    print("DEBUG: Script is imported, not run directly.") # ADDED