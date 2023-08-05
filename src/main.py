import fastapi as _fastapi
import services as _services, schemas as _schemas
import sqlalchemy.orm as _orm
from typing import List

app = _fastapi.FastAPI()

_services.create_database()


@app.post("/users", response_model=_schemas.User)
def create_user(
    user: _schemas.UserCreate, db: _orm.Session = _fastapi.Depends(_services.get_db)
):
    db_user = _services.get_user_by_email(db, user.email)
    if db_user:
        raise _fastapi.HTTPException(status_code=400, detail="Email already registered")
    return _services.create_user(db=db, user=user)


@app.get("/users/{user_id}", response_model=_schemas.User)
def get_user(user_id: int, db: _orm.Session = _fastapi.Depends(_services.get_db)):
    user = _services.get_user(db, user_id=user_id)
    if user is None:
        raise _fastapi.HTTPException(status_code=404, detail="User not found")
    return user


@app.get("/users", response_model=List[_schemas.User])
def get_users(
    skip: int = 0,
    limit: int = 100,
    db: _orm.Session = _fastapi.Depends(_services.get_db),
):
    return _services.get_users(db=db, skip=skip, limit=limit)


@app.post("/users/{user_id}/passwords", response_model=_schemas.Password)
def create_password(
    user_id: int,
    password: _schemas.PasswordCreate,
    db: _orm.Session = _fastapi.Depends(_services.get_db),
):
    db_user = _services.get_user(db, user_id=user_id)
    if db_user is None:
        raise _fastapi.HTTPException(status_code=404, detail="User not found")
    return _services.create_password(user_id=user_id, db=db, password=password)


@app.get("/users/{user_id}/passwords", response_model=List[_schemas.Password])
def get_passwords(
    user_id: int,
    db: _orm.Session = _fastapi.Depends(_services.get_db),
):
    db_user = _services.get_user(db, user_id=user_id)
    if db_user is None:
        raise _fastapi.HTTPException(status_code=404, detail="User not found")
    return _services.get_passwords(user_id=user_id, db=db)


@app.get("/users/{user_id}/passwords/{password_id}", response_model=_schemas.Password)
def get_password(
    user_id: int,
    password_id: int,
    db: _orm.Session = _fastapi.Depends(_services.get_db),
):
    db_user = _services.get_user(db=db, user_id=user_id)
    if db_user is None:
        raise _fastapi.HTTPException(status_code=404, detail="User not found")
    password = _services.get_password(db=db, user_id=user_id, password_id=password_id)
    if password is None:
        raise _fastapi.HTTPException(status_code=404, detail="Password not found")
    return password


@app.delete("/users/{user_id}/passwords/{password_id}")
def delete_password(
    user_id: int,
    password_id: int,
    db: _orm.Session = _fastapi.Depends(_services.get_db),
):
    db_user = _services.get_user(db=db, user_id=user_id)
    if db_user is None:
        raise _fastapi.HTTPException(status_code=404, detail="User not found")
    password = _services.get_password(db=db, user_id=user_id, password_id=password_id)
    if password is None:
        raise _fastapi.HTTPException(status_code=404, detail="Password not found")
    return _services.delete_password(db=db, user_id=user_id, password_id=password_id)


@app.put("/users/{user_id}/passwords/{password_id}", response_model=_schemas.Password)
def update_password(
    user_id: int,
    password_id: int,
    password: _schemas.PasswordUpdate,
    db: _orm.Session = _fastapi.Depends(_services.get_db),
):
    db_user = _services.get_user(db=db, user_id=user_id)
    if db_user is None:
        raise _fastapi.HTTPException(status_code=404, detail="User not found")
    db_password = _services.get_password(
        db=db, user_id=user_id, password_id=password_id
    )
    if db_password is None:
        raise _fastapi.HTTPException(status_code=404, detail="Password not found")
    return _services.update_password(
        db=db, user_id=user_id, password_id=password_id, password=password
    )
