import dspy
import os
import requests
import json

# The profile to scrape can be set via environment variable.
PROFILE_TO_SCRAPE = os.getenv("PROFILE_TO_SCRAPE", "https://www.linkedin.com/in/williamhgates/")

# --- Configuration (remains the same) ---
anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
if not anthropic_api_key:
    raise ValueError("ANTHROPIC_API_KEY environment variable not found.")
llm = dspy.LM("anthropic/claude-3-haiku-20240307", api_key=anthropic_api_key)
dspy.configure(lm=llm)

# --- Call our Interactive Scraper Tool ---
print("--- Calling the Interactive LinkedIn Scraper Tool ---")

try:
    scraper_payload = {"linkedin_url": PROFILE_TO_SCRAPE}
    print("Sending request to MCP Server... (A browser window may open for login)")
    response = requests.post("http://127.0.0.1:8000/tools/scrape_linkedin", json=scraper_payload, timeout=300)
    response.raise_for_status()
    scraped_data = response.json()
    
    print("\nSuccessfully received profile data from MCP Server:")
    print(json.dumps(scraped_data, indent=2))

except requests.exceptions.RequestException as e:
    print(f"\n---!!! FAILED TO CONNECT OR SCRAPE !!! ---")
    print(f"Error details: {e}\n")
    exit()

# --- Step 2: Processing the Scraped Data with DSPy ---
print("\n--- Step 2: Processing Scraped Experience with DSPy ---")

class ProcessExperience(dspy.Signature):
    """Given a raw job description, rewrite it as a single, powerful resume bullet point."""
    raw_description = dspy.InputField()
    resume_bullet_point = dspy.OutputField()

resume_processor = dspy.Predict(ProcessExperience)

for job in scraped_data.get("experience", []):
    raw_desc = job.get("description")
    prediction = resume_processor(raw_description=raw_desc)
    
    print(f"\nOriginal Description: {raw_desc}")
    print(f"AI-Generated Bullet Point: {prediction.resume_bullet_point}")
