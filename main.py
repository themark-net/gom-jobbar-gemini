import dspy
import os
import requests # Import the new library

# --- Configuration ---
anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")

if not anthropic_api_key:
    raise ValueError("ANTHROPIC_API_KEY environment variable not found. Please set it before running.")

llm = dspy.LM(
    "anthropic/claude-3-haiku-20240307",
    api_key=anthropic_api_key
)

dspy.configure(lm=llm)


# --- NEW: Call our MCP Server ---
print("Attempting to connect to the MCP Server...")
try:
    # This line sends a GET request to our running server
    response = requests.get("http://127.0.0.1:8000/")
    response.raise_for_status() # This will raise an error if the server returned an error code

    server_message = response.json().get("message")
    print(f"Successfully connected to MCP Server. Message: '{server_message}'")

except requests.exceptions.RequestException as e:
    print(f"\n---!!! FAILED TO CONNECT TO MCP SERVER !!! ---")
    print("Please ensure your mcp_server.py is running in a separate terminal.")
    print(f"Error details: {e}\n")
    # We can exit here since it can't connect
    exit()


# --- Define the "Signature" ---
class BasicQA(dspy.Signature):
    """Answer questions with short, concise answers."""
    question = dspy.InputField()
    answer = dspy.OutputField(desc="A short, factual answer.")


# --- Define the DSPy Module ---
generate_answer = dspy.Predict(BasicQA)


# --- Execute the Program ---
print("\nNow, asking the LLM a question...")
question_to_ask = "What is the primary function of a CPU in a computer?"
prediction = generate_answer(question=question_to_ask)

print(f"Question: {question_to_ask}")
print(f"Answer: {prediction.answer}")
