# Smart Meal Prep Planner & Coach

This project generates personalized 7-day meal plans using the Google Gemini Generative AI model. It takes user preferences, fitness goals, dietary restrictions, and schedule constraints to create either a basic meal name plan or a detailed plan including ingredients, recipe steps, and estimated times.

## Features

*   **Personalized Plans:** Generates 7-day meal plans tailored to individual user profiles.
*   **Handles Constraints:** Considers fitness goals (e.g., weight loss, muscle gain), dietary needs (vegetarian, allergies like nuts), taste preferences (spicy), and schedule limitations (quick lunches, dinner out).
*   **Two Detail Levels:**
    *   **Basic Plan:** Provides meal names for breakfast, lunch, and dinner each day.
    *   **Detailed Plan:** Includes meal names, ingredient lists, concise recipe steps, prep time, and cook time for each meal.
*   **JSON Output:** Saves the generated meal plan in a structured JSON format.
*   **Command-Line Interface:** Allows generating plans via simple commands in the terminal.
*   **(Planned)** Streamlit UI for easier interaction.

## Tech Stack

*   Python 3.x
*   Google Gemini API (`google-generativeai`)
*   PyYAML (for reading prompt configurations)
*   python-dotenv (for managing API keys)
*   **(Planned)** Streamlit (for the web UI)

## Project Structure


smart-meal-planner/
├── .env # Stores secret API keys (MUST NOT be committed to Git)
├── .gitignore # Specifies files/folders for Git to ignore
├── README.md # This file
├── requirements.txt # Python dependencies
├── venv/ # Python virtual environment (ignored by Git)
├── config/
│ ├── prompts.yaml # Prompt templates for the AI
│ ├── output_schema_basic.json # Expected JSON structure for basic plan
│ └── output_schema_detailed.json # Expected JSON structure for detailed plan
├── data/
│ └── examples/
│ └── user_profile_1.json # Sample user input data
├── notebooks/ # Jupyter notebooks for experimentation and testing
│ ├── 01_input_handling_test.ipynb
│ └── 02_core_plan_generation.ipynb # (Add others as created)
├── output/ # Default location for generated plans (ignored by Git)
│ └── generated_plan.json # Example output
├── scripts/
│ └── generate_plan.py # Main script to run plan generation
└── src/
└── meal_planner/ # Source code package
├── init.py
├── user_input.py # Loads user profile data
├── llm_client.py # Handles interaction with Gemini API
└── plan_generator.py # Orchestrates the plan generation logic





## Setup (Local Windows)

1.  **Prerequisites:**
    *   Python 3.8+ installed.
    *   Git installed (download from [https://git-scm.com/](https://git-scm.com/)).
    *   A Google Gemini API Key (obtain from [Google AI Studio](https://aistudio.google.com/)).

2.  **Clone the Repository (if fetching from GitHub later):**
    ```bash
    git clone <your-repository-url>
    cd smart-meal-planner
    ```
    *(Skip this step for now if just setting up locally)*

3.  **Create Virtual Environment:**
    *   Open Command Prompt or PowerShell in the `smart-meal-planner` directory.
    *   Run: `python -m venv venv`

4.  **Activate Environment:**
    *   Command Prompt: `venv\Scripts\activate.bat`
    *   PowerShell: `venv\Scripts\Activate.ps1` (You might need `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process` first).
    *   You should see `(venv)` at the start of your prompt.

5.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

6.  **Set Up API Key:**
    *   Create a file named `.env` in the project root (`smart-meal-planner`).
    *   Add your API key to the `.env` file like this:
        ```
        GEMINI_API_KEY=YOUR_ACTUAL_API_KEY_HERE
        ```
    *   **IMPORTANT:** Ensure `.env` is listed in your `.gitignore` file. **Never commit your API key!**

## Usage (Command Line)

Make sure your virtual environment is activated before running.

1.  **Show Help:**
    ```bash
    python scripts/generate_plan.py --help
    ```

2.  **Generate a Basic Plan (using defaults):**
    *   Uses `data/examples/user_profile_1.json` and `config/prompts.yaml`.
    *   Saves to `output/generated_plan.json`.
    ```bash
    python scripts/generate_plan.py
    ```

3.  **Generate a Detailed Plan:**
    *   Uses the `--detailed` flag.
    *   Specify an output file using `-o` or `--output`.
    ```bash
    python scripts/generate_plan.py --detailed -o output/my_detailed_plan.json
    ```

4.  **Use a Different Profile:**
    ```bash
    python scripts/generate_plan.py --profile path/to/your/profile.json -o output/custom_plan.json
    ```
    *(Note: Provide paths relative to the project root)*

## Configuration

*   **Prompts:** AI behavior is primarily controlled by the templates in `config/prompts.yaml`. Modify these to change instructions or expected output details.
*   **API Key:** Stored securely in the `.env` file.

## Disclaimer

This tool uses AI to generate meal plans based on provided inputs. It is intended for informational purposes only and does not constitute professional dietary or medical advice. Always consult with a qualified healthcare provider or registered dietitian before making significant changes to your diet or fitness routine.

## Future Work

*   Integrate Streamlit for a user-friendly web interface (`app.py`).
*   Implement RAG to fetch relevant YouTube cooking/nutrition videos (Phase 4).
*   Allow interactive plan adjustments via conversation (Phase 5).
*   Add more robust error handling and input validation.
*   Implement schema validation for LLM output.
