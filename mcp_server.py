from fastapi import FastAPI

# Create an instance of the FastAPI application.
# This 'app' object will handle all our API endpoints.
app = FastAPI(
    title="Gom-Jobbar MCP Server",
    description="A server hosting specialized tools like scrapers and matchers.",
    version="0.1.0"
)

# Define an API endpoint for the root URL ("/").
# The "@app.get('/')" is a "decorator" that tells FastAPI that the function
# below it should handle GET requests for the main page.
@app.get("/")
def read_root():
    """
    This is the root endpoint. It just returns a welcome message.
    """
    return {"message": "Gom-Jobbar MCP Server is running!"}
