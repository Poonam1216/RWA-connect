import asyncio
from sqlalchemy import select
from app.core.db import SessionLocal
from app.core.security import hash_password
from app.models import Society, User, UserRole

DEMO_USERS = [
    ("Society Admin", "admin@greenvalley.com", "admin"),
    ("Riya Sharma", "resident@greenvalley.com", "resident"),
    ("Ramesh Guard", "guard@greenvalley.com", "guard"),
]
DEMO_PASSWORD = "Demo@1234"

async def main():
    async with SessionLocal() as db:
        existing = await db.execute(select(User).where(User.email == DEMO_USERS[0][1]))
        if existing.scalar_one_or_none():
            print("Already seeded, skipping.")
            return

        society = Society(name="Green Valley Residency", address="Demo Address")
        db.add(society)
        await db.flush()

        for name, email, role in DEMO_USERS:
            user = User(society_id=society.id, name=name, email=email,
                        password_hash=hash_password(DEMO_PASSWORD))
            db.add(user)
            await db.flush()
            db.add(UserRole(user_id=user.id, role=role))

        await db.commit()
        print("Seeded society + 3 users. Password:", DEMO_PASSWORD)

asyncio.run(main())