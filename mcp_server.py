from fastapi import FastAPI

app = FastAPI(
    title="Gom-Jobbar MCP Server",
    description="A server hosting specialized tools like scrapers and matchers.",
    version="0.1.0"
)

# This is our old root endpoint, good for checking if the server is alive.
@app.get("/")
def read_root():
    return {"message": "Gom-Jobbar MCP Server is running!"}


# --- NEW: Our First Real Tool Endpoint ---
@app.post("/tools/scrape_linkedin")
def scrape_linkedin_profile(payload: dict):
    """
    SIMULATED: In the future, this endpoint will take a LinkedIn URL,
    launch the scraper, and return the real data. For now, it
    returns a hardcoded, mock profile.
    """
    linkedin_url = payload.get("linkedin_url")
    print(f"Received request to scrape: {linkedin_url}")

    # This is our mock data, pretending to be a real scrape result.
    mock_profile_data = {
        "fullName": "Jane Doe",
        "summary": "Experienced software engineer with 8+ years in cloud-native application development, specializing in Python and Go.",
        "experience": [
            {
                "title": "Senior Cloud Engineer",
                "company": "TechCorp Inc.",
                "duration": "Jan 2022 - Present",
                "description": "Led the migration of monolithic services to a microservices architecture on AWS. Developed CI/CD pipelines that reduced deployment time by 40%."
            },
            {
                "title": "Software Engineer",
                "company": "DataSolutions LLC",
                "duration": "Jun 2018 - Dec 2021",
                "description": "Built and maintained data processing applications using Python and Apache Spark. Implemented new features based on stakeholder requirements."
            }
        ],
        "skills": ["Python", "Go", "AWS", "Kubernetes", "Docker", "Terraform"]
    }

    print("Returning mock profile data.")
    return mock_profile_data
