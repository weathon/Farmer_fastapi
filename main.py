from re import split
from pydantic.utils import to_camel
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Table, func, select
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base
from sqlalchemy.sql.expression import false
import send_ver
from fastapi_users.db import SQLAlchemyBaseUserTable, SQLAlchemyUserDatabase
from fastapi_users.authentication import CookieAuthentication
from fastapi_users import FastAPIUsers, models
from fastapi import FastAPI, Request
import sqlalchemy
import databases
from fastapi import FastAPI, Depends
import login
import records
import routers
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session
from mydatabase import *
import security
import html
import deliveryItems
import messages
import day
from datetime import date

from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
clientDebug = True
LAXNONE = "lax"
cookie_secure = True

if clientDebug:
    from fastapi.middleware.cors import CORSMiddleware
    origins = [
        # "http://localhost.tiangolo.com",
        # "https://localhost.tiangolo.com",
        "http://localhost",
        "http://localhost:8100",
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    LAXNONE = "None"
    cookie_secure = false
# app = FastAPI()

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


# DATABASE_URL = "sqlite:///./test.db"
SECRET = "jgeyswfg8&^&TG&*ERW3245riw234r78tskiwhdlwwo95737T^&#%$6F@IE%&ISDGWUET*2"


class User(models.BaseUser):
    pass


class UserCreate(models.BaseUserCreate):
    pin: str
    # phone: str
    # farmername: str
    # farmname: str


class UserUpdate(User, models.BaseUserUpdate):
    pin: str
    # phone: str
    # farmer: str
    # farm: str


class UserDB(User, models.BaseUserDB):
    # phone: str
    # farmer: str
    # farm: str
    pass

# database = databases.Database(DATABASE_URL)


class UserTable(Base, SQLAlchemyBaseUserTable):
    # phone: str
    # farmer: str
    # farm: str
    pass


users = UserTable.__table__
user_db = SQLAlchemyUserDatabase(UserDB, database, users)

auth_backends = []

cookie_authentication = CookieAuthentication(
    secret=SECRET, lifetime_seconds=3600, cookie_samesite=LAXNONE, cookie_secure=cookie_secure)

auth_backends.append(cookie_authentication)
Base.metadata.create_all(bind=engine)
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
    print(
        f"Verification requested for user {user.id}. Verification token: {token}")
    vurl = "https://farmer.weathon.top/api/static/confirm.html?token="+token
    # with open("ver_email.html", "r") as f:
    #     html_content = f.read().replace(
    #         "{{url}}", vurl).replace("{{url}}", vurl)
    print(vurl)
    # 偶偶偶 懂了 这个token是验证用的
    # 激动  实现了  其实就是别人的API啊  现在还是这样的
    send_ver.send(user.email, token)


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
app.include_router(fastapi_users.get_users_router(),
                   prefix="/users", tags=["users"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.get("/test")
def test():
    return {"message": "I am still alive. (From GET)"}


@app.get("/records")
def get_records(crop: str, user: User = Depends(fastapi_users.current_user(active=True, verified=True))):
    # 数据库没保存
    print(user.email)
    print(crop)
    return "Please use new API"


@app.post('/creatRecord')
def same(request: records.Record,
         db: Session = Depends(get_db),
         user: User = Depends(fastapi_users.current_user(active=True, verified=True))):  # 不用call getdb

    # new_record = records.RecordBase(request)
    new_record = records.RecordBase(
        email=html.escape(user.email),
        crop=html.escape(request.crop),
        contractDate=date.today().strftime("%d-%m-%Y"),
        deliverieMonth=html.escape(request.deliverieMonth),
        buyer=html.escape(request.buyer),
        contractAmount=request.contractAmount,
        deliverieAmount=request.deliverieAmount,
        unitPrice=request.unitPrice,
        totalValue=(request.unitPrice)*(request.contractAmount),
        status=0
    )
    # print(new_record)
    db.add(new_record)
    db.commit()
    db.refresh(new_record)
    return new_record


@app.get('/getRecords')
def same(crop: str,
         db: Session = Depends(get_db),
         user: User = Depends(fastapi_users.current_user(active=True, verified=True))):  # 不用call getdb

    returnRecords = db.query(records.RecordBase).filter(
        records.RecordBase.crop == crop and records.RecordBase.email == user.email).all()
    return returnRecords


@app.get('/getMessages')
def same(archived: bool,
         db: Session = Depends(get_db),
         user: User = Depends(fastapi_users.current_user(active=True, verified=True))):  # 不用call getdb

    return db.query(messages.MessageBase).filter(messages.MessageBase.reciver == user.email).all()


@app.post('/setAllMessagesAsRead')
def read(
    db: Session = Depends(get_db),
    user: User = Depends(fastapi_users.current_user(
        active=True, verified=True))
):
    db.query(messages.MessageBase).\
        filter(messages.MessageBase.read == False and messages.MessageBase.reciver == user.email).\
        update({"read": 1})
    db.commit()
    return "OK"


@app.get("/unreadNumber")
def readnum(
    db: Session = Depends(get_db),
    user: User = Depends(fastapi_users.current_user(
        active=True, verified=True))
):
    return db.query(messages.MessageBase).\
        filter(messages.MessageBase.read ==
               False and messages.MessageBase.reciver == user.email).count()
    # chaojikun duilema


@app.get("/ifVerifited")
def ifver(
    user: User = Depends(fastapi_users.current_user(
        active=True, verified=True))
):
    return user.is_active


@app.post("/setArchive")
def archive(
    id: int,
    db: Session = Depends(get_db),
    user: User = Depends(fastapi_users.current_user(
        active=True, verified=True))
):
    db.query(messages.MessageBase).\
        filter(messages.MessageBase.archived == False and messages.MessageBase.reciver == user.email and messages.MessageBase.id == id).\
        update({"archived": 1})
    db.commit()
    return "OK"


@app.get("/getOccupiedDays")
def getOD(
    month: str,
    buyer: str,
    db: Session = Depends(get_db),
):
    return db.query(day.DayBase.day).filter(day.DayBase.buyer == buyer and day.DayBase.month == month and day.DayBase.full == false).all()


# 需要获取有没有自己  头痛 上面也要 kun jiejue chongfu chongtu exingkun
@app.get("/getDayDetail")
def getDD(
    month: str,
    inday: str,
    buyer: str,
    db: Session = Depends(get_db),
    user: User = Depends(fastapi_users.current_user(
        active=True, verified=True))
):
    ans = []  # 0 - empty  1 - self 2 - used
    periods = db.query(day.DayBase).filter(day.DayBase.buyer == buyer
                                           and day.DayBase.month == month and day.DayBase.day == inday).first().periods.split(",")
    # print(periods)
    for i in periods:
        i = int(i)  # diyigeyeyao zhelibujiance xiamian -1 huibaocu
        if i == -1:  # 先检测有没有
            ans.append(0)
        else:
            # print(i) mingmingyou a akun
            tmp = db.query(deliveryItems.DayBase).filter(
                deliveryItems.DayBase.id == i).first()  # 要验证后query
            if tmp.farmerEmail == user.email:
                ans.append(1)
            else:
                ans.append(2)
    # hysm chulide?
    return ans

# 之前的POST没有在body里 晕
# @app.post("/newDelivery")


def newDelivery(
    request: deliveryItems.Day,
    db: Session = Depends(get_db),
    user: User = Depends(fastapi_users.current_user(
        active=True, verified=True))
):
    # 忘记处理 Day表了， 而且要在前面
    # 检查是否可用 可以的话看占用了多少 然后占用数量加1（不再需要bool?）加一后检测bool,xiugai huang hysm +
    periods = db.query(day.DayBase).filter(day.DayBase.buyer == request.buyer
                                           and day.DayBase.month == request.month and day.DayBase.day == request.inday).first().periods

    # 先检查是否可用.
    perlist = periods.split(",")
    if(perlist[request.periodNumber] != -1):
        # 占用了
        return "Error"
    new_de = deliveryItems.DayBase(
        farmerEmail=html.escape(user.email),  # 注册时就需要?
        buyer=html.escape(request.buyer),
        amount=request.amount,
        moisture=request.moisture,
        crop=html.escape(request.crop),
        date=html.escape(request.date),
        periodNumber=request.periodNumber,
        thedate=date.today().strftime("%d-%m-%Y")
    )
    # print(new_record)
    db.add(new_de)
    db.commit()
    db.refresh(new_de)
    # 插入id并且修改bool
    perlist[request.periodNumber] = new_de.id
    db.query(day.DayBase).filter(day.DayBase.buyer == request.buyer
                                 and day.DayBase.month == request.month and day.DayBase.day == request.inday).update({"periods": str(perlist)[1:-1]})

    if(db.query(day.DayBase).filter(day.DayBase.buyer == request.buyer
                                    and day.DayBase.month == request.month and day.DayBase.day == request.inday).first().count >= 48):
        db.query(day.DayBase).filter(day.DayBase.buyer == request.buyer
                                     and day.DaqyBase.month == request.month and day.DayBase.day == request.inday).update({"full": 1})

    return new_de
    # huangkuhysm

