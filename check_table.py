"""
Check if the taken_birth_control_pills column exists in the database
"""

from app.database import engine
from sqlalchemy import text, inspect

def check_table_structure():
    """Check if the column exists"""
    try:
        inspector = inspect(engine)
        columns = [col['name'] for col in inspector.get_columns('assessments')]
        
        print("Columns in 'assessments' table:")
        for col in columns:
            print(f"  - {col}")
        
        if 'taken_birth_control_pills' in columns:
            print("\n✅ Column 'taken_birth_control_pills' exists!")
        else:
            print("\n❌ Column 'taken_birth_control_pills' is MISSING!")
            print("\nRun: python init_db.py")
        
        return 'taken_birth_control_pills' in columns
    except Exception as e:
        print(f"Error checking table: {e}")
        return False

if __name__ == "__main__":
    check_table_structure()

