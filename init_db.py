"""
Initialize database tables
Run this script to create all database tables
"""

from app.database import engine, Base
from app import models

def init_database():
    """Create all database tables"""
    try:
        # Create all tables
        Base.metadata.create_all(bind=engine)
        print("✅ Database tables created successfully!")
        print("\nTables created:")
        print("  - assessments")
        print("\nYou can now run the FastAPI server.")
    except Exception as e:
        print(f"❌ Error creating database tables: {e}")
        print("\nTroubleshooting:")
        print("  1. Check PostgreSQL is running")
        print("  2. Verify DATABASE_URL in .env file is correct")
        print("  3. Ensure database 'ovasense_db' exists")
        raise

if __name__ == "__main__":
    init_database()

