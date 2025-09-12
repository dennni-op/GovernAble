# api/services/storage.py
import json
# These are tools from SQLAlchemy, the most popular Python library for talking to databases.
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker, Mapped, mapped_column
from sqlalchemy import Integer, String, Text, DateTime, func
# Import our settings to get the database URL.
from api.config import settings
DATABASE_URL = settings.DATABASE_URL
# Create the 'engine', which is the main connection point to our database.
# We use 'create_async_engine' because our API is asynchronous.
engine = create_async_engine(DATABASE_URL)
# This creates a factory for database sessions. A session is like a single conversation with the database.
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
# This is a base class that our database models will inherit from.
Base = declarative_base()
# This defines the 'scan_results' table in our database.
class ScanResult(Base):
    __tablename__ = "scan_results"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    filename: Mapped[str] = mapped_column(String(256), nullable=True)
    # We'll store the list of findings as a JSON string in a text field.
    findings: Mapped[str] = mapped_column(Text)
    scanned_at: Mapped = mapped_column(DateTime(timezone=True), server_default=func.now())
# A function to create the database tables if they don't exist.
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
# A function to save a scan result to the database.
async def save_scan(filename: str, findings: dict):
    # Start a new conversation/session with the database.
    async with AsyncSessionLocal() as session:
        # Create a new ScanResult record. We convert the findings dictionary to a JSON string.
        record = ScanResult(filename=filename, findings=json.dumps(findings))
        session.add(record) # Add the new record to the session.
        await session.commit() # Commit (save) the changes to the database.
        return record.id