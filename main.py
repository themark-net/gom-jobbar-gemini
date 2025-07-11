import dspy
import os
import requests
import json # Import json to pretty-print the output

# --- Configuration (remains the same) ---
anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")

if not anthropic_api_key:
    raise ValueError("ANTHROPIC_API_KEY environment variable not found. Please set it before running.")

llm = dspy.LM(
    "anthropic/claude-3-haiku-20240307",
    api_key=anthropic_api_key
)

dspy.configure(lm=llm)


# --- Call our NEW Scraper Tool ---
print("--- Step 1: Calling the LinkedIn Scraper Tool ---")
try:
    # We now send a POST request to the new endpoint
    # We also send a "payload" with the URL we want to scrape
    scraper_payload = {"linkedin_url": "https://www.linkedin.com/in/janedoe-example"}
    response = requests.post("http://127.0.0.1:8000/tools/scrape_linkedin", json=scraper_payload)
    response.raise_for_status()
    
    # The server returns the profile data, which we store in a variable
    scraped_data = response.json()
    
    print("Successfully received profile data from MCP Server:")
    # Use json.dumps to print the dictionary in a nicely formatted way
    print(json.dumps(scraped_data, indent=2))


except requests.exceptions.RequestException as e:
    print(f"\n---!!! FAILED TO CONNECT TO MCP SERVER !!! ---")
    print("Please ensure your mcp_server.py is running in a separate terminal.")
    print(f"Error details: {e}\n")
    exit()

# --- For now, we'll stop here. The DSPy part will come next. ---
print("\n--- Next Step: Process this data with DSPy ---")

# (We will add the DSPy logic to parse this data in our next step)
