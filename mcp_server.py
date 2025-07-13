from fastapi import FastAPI
import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.common.exceptions import NoSuchElementException

# --- CORRECTED PATH: Use the local, relative path for our session data ---
LINKEDIN_PROFILE_PATH = "./linkedin_session_profile"

app = FastAPI(title="Gom-Jobbar MCP Server")

# This is the new, powerful scraping function from our last step. It is correct.
def get_profile_data(driver, profile_url):
    """
    Extracts detailed information (name, summary, experience) from a
    loaded LinkedIn profile page.
    """
    print(f"Navigating to profile: {profile_url}")
    driver.get(profile_url)
    time.sleep(5) 
    
    try:
        name = driver.find_element(By.TAG_NAME, "h1").text
    except NoSuchElementException:
        name = "Name not found"

    try:
        # This selector is more robust for the "About" section.
        about_element = driver.find_element(By.XPATH, "//div[contains(@class, 'pv-about-section')]//p")
        summary = about_element.text.strip()
    except NoSuchElementException:
        summary = "About section not found."

    experience_list = []
    try:
        # Find all the individual job entries. This selector is more robust.
        job_elements = driver.find_elements(By.XPATH, "//li[contains(@class, 'pv-entity__position-group-pager')]")
        
        for job_element in job_elements:
            try:
                # We extract the text from the parent element and split it, as the inner classes can be inconsistent.
                lines = job_element.text.split('\n')
                title = lines[0] if len(lines) > 0 else "Title not found"
                company = lines[1] if len(lines) > 1 else "Company not found"
                duration = lines[2] if len(lines) > 2 else "Duration not found"
                description = job_element.find_element(By.CLASS_NAME, "pv-entity__description").text if job_element.find_elements(By.CLASS_NAME, "pv-entity__description") else "Description not found"
                
                experience_list.append({
                    "title": title,
                    "company": company,
                    "duration": duration,
                    "description": description
                })
            except Exception:
                continue
    except NoSuchElementException:
        pass

    return {
        "fullName": name,
        "scrapedFrom": profile_url,
        "summary": summary,
        "experience": experience_list,
    }


# This is the correct endpoint logic using the local profile path.
@app.post("/tools/scrape_linkedin")
def scrape_linkedin_profile_interactive(payload: dict):
    profile_url = payload.get("linkedin_url")
    if not profile_url:
        return {"error": "Missing profile_url in payload."}

    os.makedirs(LINKEDIN_PROFILE_PATH, exist_ok=True)
    
    print(f"Initializing WebDriver with local profile: '{LINKEDIN_PROFILE_PATH}'")
    options = ChromeOptions()
    options.add_argument(f"--user-data-dir={LINKEDIN_PROFILE_PATH}")
    
    service = Service(executable_path='./chromedriver')
    driver = webdriver.Chrome(service=service, options=options)

    try:
        driver.get("https://www.linkedin.com/feed/")
        time.sleep(2)
        
        if "/feed/" not in driver.current_url:
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
