# Fix Database Schema Error

If you're seeing an error when submitting the assessment, it's likely because the database table doesn't have the new `taken_birth_control_pills` column.

## Quick Fix

Run this command to recreate the database tables with the new column:

```bash
python init_db.py
```

## Alternative: Manual SQL Fix

If you want to keep existing data, you can add the column manually:

```sql
-- Connect to your database
psql -U postgres -d ovasense_db

-- Add the new column
ALTER TABLE assessments ADD COLUMN taken_birth_control_pills BOOLEAN DEFAULT FALSE;

-- Exit
\q
```

## Verify Fix

After running the fix, try submitting the assessment again. The error should be resolved.

