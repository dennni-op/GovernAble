# api/config.py
from pydantic import BaseSettings, Field

class Settings(BaseSettings):
    # --- Project Info ---
    # This is for basic, non-sensitive information about your application.
    # It's useful for things like setting the title in your API documentation.
    PROJECT_NAME: str = "GovernAble API"
    API_V1_STR: str = "/api/v1"

    # --- Security & Secrets ---
    # This is the most critical section. These are values that must be kept secret.
    # The secret API key clients must use to access your service.
    # The default 'dev_key' is just for development. In production, you would set
    # this using an environment variable (GA_API_KEY) for security.
    API_KEY: str = Field("dev_key", env="GA_API_KEY")

    # A comma-separated string of websites that are allowed to connect to this API.
    # For development, "*" (allowing everyone) is okay.
    # For production, you MUST lock this down (e.g., "https://app.governable.com").
    CORS_ORIGINS: str = Field("*", env="CORS_ORIGINS")

    # --- Database ---
    # This tells your application how to find and log into your database.
    # The default is a simple file-based SQLite database, which is great for development.
    # For production, you would change this to a PostgreSQL or MySQL connection string.
    DATABASE_URL: str = Field("sqlite+aiosqlite:///./governable.db", env="DATABASE_URL")

    # --- Application Tuning Knobs ---
    # These are adjustable parameters that control your app's behavior.
    # It's good practice to make values like this configurable instead of hard-coding them.
    # The maximum file size (in bytes) that the /scan/file endpoint will accept.
    MAX_SCAN_FILE_BYTES: int = Field(5_000_000, env="MAX_SCAN_FILE_BYTES") # Default: 5MB

    class Config:
        # This tells Pydantic to also load these settings from a file named .env
        # This allows you to override the defaults for production without changing the code.
        env_file = ".env"

# Create a single, reusable instance of the settings that the rest of our app can use.
settings = Settings()