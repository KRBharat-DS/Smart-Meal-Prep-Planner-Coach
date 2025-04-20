import os
import google.generativeai as genai
from dotenv import load_dotenv
import json # Import json for parsing potential JSON output

# Load environment variables from .env file
load_dotenv()

# Configure the generative AI client
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY not found in .env file or environment variables.")

genai.configure(api_key=api_key)

# --- Configuration ---
# Choose the model appropriate for text generation and potentially JSON output
# 'gemini-pro' is a good starting point.
# Models supporting explicit JSON mode might be named differently (e.g., check Gemini docs)
MODEL_NAME = "gemini-1.5-pro-latest" # Or "gemini-pro" if 1.5 isn't available/needed yet

# Define generation configuration for potentially forcing JSON output
# Note: Explicit JSON mode might require specific model versions or settings.
# Refer to Google AI documentation for the latest on enforcing JSON.
# This is a general approach; specific JSON mode might use different parameters.
GENERATION_CONFIG_JSON = {
  "temperature": 0.5, # Adjust creativity (lower is more deterministic)
  "top_p": 0.95,
  "top_k": 40,
  "max_output_tokens": 2048, # Adjust as needed for plan length
  "response_mime_type": "application/json", # Request JSON output
}

# --- Client Function ---

def generate_text_with_retry(prompt_text, generation_config=None, safety_settings=None, retries=2):
    """
    Calls the Gemini API to generate text based on a prompt, with retries.

    Args:
        prompt_text (str): The input prompt for the model.
        generation_config (dict, optional): Configuration for generation (temp, tokens, etc.).
                                            Defaults to a basic config if None.
        safety_settings (list, optional): Configuration for safety filters. Defaults to None.
        retries (int): Number of times to retry on specific errors.

    Returns:
        str: The generated text content from the model, or None if generation fails after retries.
    """
    if generation_config is None:
        # Default config if none provided (might not force JSON here)
        generation_config = {
            "temperature": 0.7,
            "top_p": 0.95,
            "top_k": 40,
            "max_output_tokens": 20000,
            "response_mime_type": "application/json" # Default to text/plain if not JSON
        }

    model = genai.GenerativeModel(
        model_name=MODEL_NAME,
        generation_config=generation_config,
        safety_settings=safety_settings
        # system_instruction="You are a helpful meal planning assistant." # Optional: Set system-level instructions
    )

    attempt = 0
    while attempt <= retries:
        try:
            print(f"\n--- Calling Gemini API (Attempt {attempt + 1}/{retries + 1}) ---")
            response = model.generate_content(prompt_text)
            print("--- Gemini API Call Successful ---")

            # Basic check if response has text content
            if response.parts:
                 # Accessing the text directly, assuming it's the first part
                 # If using JSON mode, this should ideally be the JSON string
                generated_content = response.text
                # print(f"Raw Response Text:\n{generated_content[:500]}...") # Optional: Print start of raw response
                return generated_content
            else:
                 # Handle cases where the response might be blocked or empty
                 print("Warning: Response received but contains no usable parts.")
                 # Check for blocking reasons if available
                 if response.prompt_feedback and response.prompt_feedback.block_reason:
                     print(f"Prompt blocked due to: {response.prompt_feedback.block_reason}")
                 # Check candidates for finish reasons
                 if response.candidates and response.candidates[0].finish_reason != 'STOP':
                     print(f"Generation stopped due to: {response.candidates[0].finish_reason}")
                 return None # Indicate failure or empty response

        except Exception as e:
            # Catching a broad range of potential API errors
            print(f"Error during Gemini API call (Attempt {attempt + 1}): {e}")
            attempt += 1
            if attempt > retries:
                print("Max retries reached. Generation failed.")
                return None
            print("Retrying...")
            # Consider adding a small delay here before retrying: time.sleep(1)

    return None # Should not be reached if loop logic is correct, but acts as fallback

# --- Helper to Parse JSON ---
def parse_json_output(text_output):
    """
    Attempts to parse a string assumed to contain JSON into a Python dictionary.

    Args:
        text_output (str): The string output from the LLM.

    Returns:
        dict: The parsed dictionary, or None if parsing fails or input is None.
    """
    if not text_output:
        print("Error: No text output received from LLM to parse.")
        return None

    try:
        # Sometimes the LLM might wrap the JSON in markdown ```json ... ```
        if text_output.strip().startswith("```json"):
            print("Detected JSON wrapped in markdown, attempting to extract.")
            # Extract content between the first ```json and the last ```
            json_str = text_output.split("```json", 1)[1].rsplit("```", 1)[0].strip()
        elif text_output.strip().startswith("{") and text_output.strip().endswith("}"):
             # Assume it's already a JSON string if it starts/ends with braces
             json_str = text_output.strip()
        else:
            # If it doesn't look like JSON, maybe the LLM failed the instruction
            print("Warning: Output doesn't look like JSON. Attempting direct parse anyway.")
            json_str = text_output.strip() # Try parsing directly just in case

        parsed_json = json.loads(json_str)
        print("Successfully parsed JSON output.")
        return parsed_json
    except json.JSONDecodeError as e:
        print(f"Error: Failed to decode JSON from LLM output. Error: {e}")
        print(f"Problematic Text (first 500 chars):\n{text_output[:500]}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred during JSON parsing: {e}")
        return None


