"""
Test database connection
Run this to verify your database setup is correct
"""

from app.database import engine, SessionLocal
from sqlalchemy import text

def test_connection():
    """Test database connection"""
    print("Testing database connection...")
    print("=" * 50)
    
    try:
        # Test connection
        with engine.connect() as conn:
            result = conn.execute(text("SELECT version()"))
            version = result.fetchone()[0]
            print(f"✅ Connected to PostgreSQL!")
            print(f"   Version: {version.split(',')[0]}")
        
        # Test database exists
        with engine.connect() as conn:
            result = conn.execute(text("SELECT current_database()"))
            db_name = result.fetchone()[0]
            print(f"✅ Current database: {db_name}")
        
        # Test table creation (if tables don't exist)
        try:
            with engine.connect() as conn:
                result = conn.execute(text("SELECT COUNT(*) FROM assessments"))
                count = result.fetchone()[0]
                print(f"✅ Table 'assessments' exists with {count} records")
        except Exception:
            print("ℹ️  Table 'assessments' doesn't exist yet (this is OK)")
            print("   Run 'python init_db.py' to create tables")
        
        print("\n" + "=" * 50)
        print("✅ Database connection test passed!")
        return True
        
    except Exception as e:
        print(f"\n❌ Database connection failed!")
        print(f"   Error: {str(e)}")
        print("\nTroubleshooting:")
        print("  1. Is PostgreSQL running?")
        print("  2. Check your .env file has correct DATABASE_URL")
        print("  3. Verify database 'ovasense_db' exists")
        print("  4. Check username and password are correct")
        return False

if __name__ == "__main__":
    test_connection()

