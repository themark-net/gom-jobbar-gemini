import dspy
import os

# --- Configuration ---
# IMPORTANT: Replace "YOUR_ANTHROPIC_API_KEY" with your actual Claude API key.
# For better security, it's recommended to set this as an environment variable.
os.environ["ANTHROPIC_API_KEY"] = "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"
# If you've set the environment variable, you can remove the api_key parameter below.
claude_haiku = dspy.Claude(model='claude-3-haiku-20240307', api_key="YOUR_ANTHROPIC_API_KEY")

# Configure DSPy to use the Claude Haiku model as the language model.
dspy.configure(lm=claude_haiku)

# --- Define the "Signature" ---
# A signature defines the input/output behavior of our DSPy program.
# It tells the LLM what we want it to do.
class BasicQA(dspy.Signature):
    """Answer questions with short, concise answers."""
    question = dspy.InputField()
    answer = dspy.OutputField(desc="A short, factual answer.")

# --- Define the DSPy Module ---
# A module is a building block of a DSPy program. `dspy.Predict` is the simplest one.
generate_answer = dspy.Predict(BasicQA)

# --- Execute the Program ---
# Let's run our program with a sample question.
question_to_ask = "What is the primary function of a CPU in a computer?"
prediction = generate_answer(question=question_to_ask)

print(f"Question: {question_to_ask}")
print(f"Answer: {prediction.answer}")
