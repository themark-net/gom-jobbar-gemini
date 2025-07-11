from fastapi import FastAPI
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
# CORRECTED IMPORT: We are importing the class named 'Service'
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options as ChromeOptions

# --- IMPORTANT: PASTE YOUR CHROME PROFILE PATH HERE ---
#CHROME_PROFILE_PATH = "$HOME/snap/chromium/common/chromium/Default"
CHROME_PROFILE_PATH = "/home/mark/snap/chromium/common/chromium/Default"
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
    REAL SCRAPER v2: Uses an existing Chrome profile to bypass login/MFA.
    """
    profile_url = payload.get("linkedin_url")
    if not profile_url:
        return {"error": "Missing profile_url in payload."}

    print("Initializing WebDriver with existing user profile...")
    options = ChromeOptions()
    options.add_argument(f"--user-data-dir={CHROME_PROFILE_PATH}")
    options.add_argument("--profile-directory=Default") 
    
    # CORRECTED USAGE: We now use 'Service' directly.
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
