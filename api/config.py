# api/config.py
from pydantic import BaseSettings, Field
from typing import Literal

class Settings(BaseSettings):
    # --- Project Info ---
    PROJECT_NAME: str = "GovernAble AI Governance Engine"
    API_V1_STR: str = "/api/v1"
    ENV: Literal["development", "staging", "production"] = Field("development", env="ENV")
    
    # --- Security & Authentication ---
    API_KEY: str = Field("dev_key", env="GA_API_KEY")
    CORS_ORIGINS: str = Field("*", env="CORS_ORIGINS")
    
    # --- AI Governance Settings ---
    DEFAULT_GOVERNANCE_POLICY: Literal["strict", "redact", "warn"] = Field(
        "strict", 
        env="DEFAULT_POLICY",
        description="Default policy for AI governance: strict=BLOCK, redact=REDACT, warn=WARN"
    )
    
    ALLOWED_AI_SERVICES: str = Field(
        "openai,anthropic", 
        env="ALLOWED_AI_SERVICES",
        description="Comma-separated list of approved AI services"
    )
    
    # --- Database ---
    DATABASE_URL: str = Field("sqlite+aiosqlite:///./governable.db", env="DATABASE_URL")
    
    # --- Scanning Limits ---
    MAX_SCAN_FILE_BYTES: int = Field(5_000_000, env="MAX_SCAN_FILE_BYTES")
    MAX_PROMPT_LENGTH: int = Field(100_000, env="MAX_PROMPT_LENGTH", description="Max AI prompt length")
    
    # --- Audit & Compliance ---
    ENABLE_AUDIT_LOGGING: bool = Field(True, env="ENABLE_AUDIT_LOGGING")
    AUDIT_LOG_RETENTION_DAYS: int = Field(90, env="AUDIT_LOG_RETENTION_DAYS")
    
    # --- Alerts & Notifications ---
    SLACK_WEBHOOK_URL: str = Field("", env="SLACK_WEBHOOK_URL")
    ALERT_ON_BLOCKED_REQUESTS: bool = Field(True, env="ALERT_ON_BLOCKED")
    
    class Config:
        env_file = ".env"
        case_sensitive = False

    def is_ai_service_allowed(self, service: str) -> bool:
        """Check if AI service is in the allowlist"""
        allowed = [s.strip().lower() for s in self.ALLOWED_AI_SERVICES.split(",")]
        return service.lower() in allowed

settings = Settings()