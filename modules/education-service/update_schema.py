import asyncio
import os
import sys

# Add parent directory to path to allow importing app modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.database import engine, Base
from app.models import School, GreenCourse, Review

async def update_schema():
    print("🔄 Updating database schema...")
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        print("✅ Schema updated successfully!")
    except Exception as e:
        print(f"❌ Error updating schema: {e}")
    finally:
        await engine.dispose()

if __name__ == "__main__":
    asyncio.run(update_schema())
