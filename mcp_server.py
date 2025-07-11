from fastapi import FastAPI
import time
import os  # Import the os library
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options as ChromeOptions

# --- CORRECTED PATH HANDLING ---
# Use os.path.expanduser to correctly resolve the home directory path.
# We point to the parent directory of "Default".
chrome_user_data_dir = os.path.expanduser("~/snap/chromium/common/chromium")

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
                "title": "Real Scrape Successful",
                "company": "Gom-Jobbar App",
                "duration": "Just now",
                "description": f"Successfully launched authenticated browser and scraped the name '{name}'."
            }
        ]
    }

@app.post("/tools/scrape_linkedin")
def scrape_linkedin_profile_real(payload: dict):
    """
    REAL SCRAPER v3: Correctly uses the user's existing Chrome profile.
    """
    profile_url = payload.get("linkedin_url")
    if not profile_url:
        return {"error": "Missing profile_url in payload."}

    print(f"Initializing WebDriver with user data dir: {chrome_user_data_dir}")
    options = ChromeOptions()
    # Tell Selenium where to find all the user profiles
    options.add_argument(f"--user-data-dir={chrome_user_data_dir}")
    # Tell Selenium which specific profile to use
    options.add_argument("--profile-directory=Default")

    # This is a flag from your chrome://version page that might help
    options.add_argument("--password-store=basic") 
    
    service = Service(executable_path='./chromedriver')
    driver = webdriver.Chrome(service=service, options=options)

    try:
        profile_data = get_profile_data(driver, profile_url)
        return profile_data
    except Exception as e:
        print(f"An error occurred during scraping: {e}")
        return {"error": "Failed to scrape LinkedIn."}
    finally:
        print("Closing WebDriver.")
        driver.quit()
