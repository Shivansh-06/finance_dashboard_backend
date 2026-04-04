from db.base import Base
from db.session import engine
from fastapi import FastAPI
from api.routes import auth, dashboard, finance, users
from models import user, role, financial_record
from models.role import Role
from db.session import SessionLocal


Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth.router)
app.include_router(finance.router)
app.include_router(dashboard.router)
app.include_router(users.router)

def seed_roles():
    db = SessionLocal()

    roles = ["Admin", "Analyst", "Viewer"]

    for r in roles:
        if not db.query(Role).filter(Role.name == r).first():
            db.add(Role(name=r))

    db.commit()
    db.close()

seed_roles()