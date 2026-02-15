"""
Add the taken_birth_control_pills column to existing assessments table
"""

from app.database import engine
from sqlalchemy import text

def add_column():
    """Add the missing column"""
    try:
        with engine.connect() as conn:
            # Check if column exists first
            result = conn.execute(text("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name='assessments' 
                AND column_name='taken_birth_control_pills'
            """))
            
            if result.fetchone():
                print("✅ Column 'taken_birth_control_pills' already exists!")
                return
            
            # Add the column
            conn.execute(text("""
                ALTER TABLE assessments 
                ADD COLUMN taken_birth_control_pills BOOLEAN DEFAULT FALSE
            """))
            conn.commit()
            print("✅ Column 'taken_birth_control_pills' added successfully!")
            print("   Existing data preserved with default value FALSE")
    except Exception as e:
        print(f"❌ Error adding column: {e}")
        raise

if __name__ == "__main__":
    add_column()

