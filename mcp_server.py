from fastapi import FastAPI
import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options as ChromeOptions

# Define a path for a dedicated profile directory right inside our project folder.
LINKEDIN_PROFILE_PATH = "./linkedin_session_profile"

app = FastAPI(title="Gom-Jobbar MCP Server")

def get_profile_data(driver, profile_url):
    """Extracts data from a loaded LinkedIn profile page."""
    print(f"Navigating to profile: {profile_url}")
    driver.get(profile_url)
    time.sleep(4)

    try:
        name_element = driver.find_element(By.TAG_NAME, "h1")
        name = name_element.text
    except Exception as e:
        name = "Could not find name"
        print(f"Error scraping name: {e}")

    return {
        "fullName": name,
        "scrapedFrom": profile_url,
        "summary": "This is a placeholder summary. A full scraper would extract the real one.",
        "experience": [
            {
                "title": "Interactive Login Successful",
                "company": "Gom-Jobbar App",
                "duration": "Just now",
                "description": f"Successfully used the interactive login session to scrape the name '{name}'."
            }
        ]
    }

@app.post("/tools/scrape_linkedin")
def scrape_linkedin_profile_interactive(payload: dict):
    """
    Uses a dedicated, local browser profile and prompts the user
    to log in manually the first time.
    """
    profile_url = payload.get("linkedin_url")
    if not profile_url:
        return {"error": "Missing profile_url in payload."}

    # Ensure the profile directory exists before we use it.
    os.makedirs(LINKEDIN_PROFILE_PATH, exist_ok=True)
    
    print(f"Initializing WebDriver with local profile: '{LINKEDIN_PROFILE_PATH}'")
    options = ChromeOptions()
    options.add_argument(f"--user-data-dir={LINKEDIN_PROFILE_PATH}")
    
    service = Service(executable_path='./chromedriver')
    driver = webdriver.Chrome(service=service, options=options)

    try:
        # Check if we are already logged in by looking for the "feed" URL.
        driver.get("https://www.linkedin.com/feed/")
        time.sleep(2)
        
        is_logged_in = "/feed/" in driver.current_url

        if not is_logged_in:
            print("\n" + "="*50)
            print(">>> ACTION REQUIRED: Please log in to LinkedIn <<<")
            print("="*50 + "\n")
            driver.get("https://www.linkedin.com/login")
            input("After you have successfully logged in, press Enter in this terminal to continue...")
        else:
            print("Previously saved login session found. Proceeding to scrape.")

        profile_data = get_profile_data(driver, profile_url)
        return profile_data
    except Exception as e:
        print(f"An error occurred during scraping: {e}")
        return {"error": "Failed to scrape LinkedIn."}
    finally:
        print("Closing WebDriver.")
        driver.quit()
