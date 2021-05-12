from fastapi import FastAPI, Depends
import login
import records
import routers
app = FastAPI()

"""
Enjoy the fight that will give the right to be free
Do you hear the people sing
Singing the song of the angry man
It is the music of the people that will not be salary again
When the beaing of you rheart
Echo the beatong of the drum
——Les Misérables | Do You Hear the People Sing?
"""
# 本地修改的库 还是被引用到python的了

import databases
import sqlalchemy
from fastapi import FastAPI, Request
from fastapi_users import FastAPIUsers, models
from fastapi_users.authentication import CookieAuthentication
from fastapi_users.db import SQLAlchemyBaseUserTable, SQLAlchemyUserDatabase
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Table, func, select

DATABASE_URL = "sqlite:///./test.db"
SECRET = "jgeyswfg8&^&TG&*ERW3245riw234r78tskiwhdlwwo95737T^&#%$6F@IE%&ISDGWUET*2"

class User(models.BaseUser): 
    pass

class UserCreate(models.BaseUserCreate):
    pin: str

class UserUpdate(User, models.BaseUserUpdate):
    pass

class UserDB(User, models.BaseUserDB):
    pass

Base: DeclarativeMeta = declarative_base()
database = databases.Database(DATABASE_URL)

class UserTable(Base, SQLAlchemyBaseUserTable):
    pass

engine = sqlalchemy.create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)
Base.metadata.create_all(engine)


users = UserTable.__table__
user_db = SQLAlchemyUserDatabase(UserDB, database, users)

auth_backends = []

cookie_authentication = CookieAuthentication(secret=SECRET, lifetime_seconds=3600)

auth_backends.append(cookie_authentication)

fastapi_users = FastAPIUsers(
    user_db,
    auth_backends,
    User,
    UserCreate,
    UserUpdate,
    UserDB,
)

def on_after_register(user: UserDB, request: Request):
    print(f"User {user.id} has registered.")


def on_after_forgot_password(user: UserDB, token: str, request: Request):
    print(f"User {user.id} has forgot their password. Reset token: {token}")


def after_verification_request(user: UserDB, token: str, request: Request):
    print(f"Verification requested for user {user.id}. Verification token: {token}")



app.include_router(
    fastapi_users.get_auth_router(cookie_authentication), prefix="/auth/jwt", tags=["auth"]
)
app.include_router(
    fastapi_users.get_register_router(on_after_register), prefix="/auth", tags=["auth"]
)
app.include_router(
    fastapi_users.get_reset_password_router(
        SECRET, after_forgot_password=on_after_forgot_password
    ),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_verify_router(
        SECRET, after_verification_request=after_verification_request
    ),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(fastapi_users.get_users_router(), prefix="/users", tags=["users"])



@app.get("/test")
def test():
    return {"message": "I am still alive. (From GET)"}

@app.get("/records")
def records(user: User = Depends(fastapi_users.current_user(active=True, verified=True))):
    pass

