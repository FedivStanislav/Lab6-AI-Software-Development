
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field, EmailStr

app = FastAPI(
    title="AI Software Development Lab",
    description="REST API for user management and data validation",
    version="1.0.0"
)


class UserCreate(BaseModel):
    name: str = Field(min_length=2, max_length=50)
    email: EmailStr
    age: int = Field(ge=18, le=100)


class User(BaseModel):
    id: int
    name: str
    email: EmailStr
    age: int


users: dict[int, User] = {}
next_user_id = 1


@app.get("/")
def home():
    return {"message": "AI Software Development API is running"}


@app.post("/users", response_model=User, status_code=201)
def create_user(user_data: UserCreate):
    global next_user_id

    if any(u.email == user_data.email for u in users.values()):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with this email already exists"
        )

    user = User(id=next_user_id, **user_data.model_dump())
    users[next_user_id] = user
    next_user_id += 1

    return user


@app.get("/users", response_model=list[User])
def get_users():
    return list(users.values())


@app.get("/users/{user_id}", response_model=User)
def get_user(user_id: int):
    if user_id not in users:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return users[user_id]
