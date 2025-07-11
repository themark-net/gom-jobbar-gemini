import dspy
import os

# --- Configuration ---
# This part remains correct.
anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")

if not anthropic_api_key:
    raise ValueError("ANTHROPIC_API_KEY environment variable not found. Please set it before running.")

# --- THIS IS THE CORRECTED MODEL INITIALIZATION ---
#
# We use the unified `dspy.LM` class and pass the provider and model name as a string.
# This is the new, standardized way to call any model in DSPy.
#
llm = dspy.LM(
    "anthropic/claude-3-haiku-20240307",
    api_key=anthropic_api_key
)

# Configure DSPy to use our initialized language model.
dspy.configure(lm=llm)


# --- Define the "Signature" (This remains the same) ---
class BasicQA(dspy.Signature):
    """Answer questions with short, concise answers."""
    question = dspy.InputField()
    answer = dspy.OutputField(desc="A short, factual answer.")


# --- Define the DSPy Module (This remains the same) ---
generate_answer = dspy.Predict(BasicQA)


# --- Execute the Program (This remains the same) ---
question_to_ask = "What is the primary function of a CPU in a computer?"
prediction = generate_answer(question=question_to_ask)

print(f"Question: {question_to_ask}")
print(f"Answer: {prediction.answer}")
