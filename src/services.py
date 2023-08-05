import pyotp
import database as _database, models as _models, schemas as _schemas
import sqlalchemy.orm as _orm
from passlib.hash import pbkdf2_sha256 as _hasher
from password_generator import Password_generator


def create_database():
    return _database.Base.metadata.create_all(bind=_database.engine)


def get_db():
    db = _database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_user_by_email(db: _orm.Session, email: str):
    return db.query(_models.User).filter(_models.User.email == email).first()


def create_user(user: _schemas.UserCreate, db: _orm.Session):
    hashed_password = _hasher.hash(user.password)
    if user.tfa:
        tfa_key = str(pyotp.random_base32())
    else:
        tfa_key = " "

    db_user = _models.User(
        email=user.email,
        hashed_password=hashed_password,
        tfa=user.tfa,
        tfa_secret=tfa_key,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user(db: _orm.Session, user_id: int):
    return db.query(_models.User).filter(_models.User.id == user_id).first()


def get_users(db: _orm.Session, skip: int = 0, limit: int = 100):
    return db.query(_models.User).offset(skip).limit(limit).all()


def create_password(user_id: int, password: _schemas.PasswordCreate, db: _orm.Session):
    db_password = _models.Password(
        name=password.name,
        value=Password_generator.generate(password.length),
        owner_id=user_id,
    )
    db.add(db_password)
    db.commit()
    db.refresh(db_password)
    return db_password


def get_passwords(user_id: int, db: _orm.Session):
    return db.query(_models.Password).filter(_models.Password.owner_id == user_id).all()


def get_password(user_id: int, password_id: int, db: _orm.Session):
    return (
        db.query(_models.Password)
        .filter(_models.Password.owner_id == user_id)
        .filter(_models.Password.id == password_id)
        .first()
    )


def delete_password(user_id: int, password_id: int, db: _orm.Session):
    db_password = (
        db.query(_models.Password)
        .filter(_models.Password.owner_id == user_id)
        .filter(_models.Password.id == password_id)
        .first()
    )
    db.delete(db_password)
    db.commit()
    return True


def update_password(
    user_id: int, password_id: int, password: _schemas.PasswordUpdate, db: _orm.Session
):
    db_password = (
        db.query(_models.Password)
        .filter(_models.Password.owner_id == user_id)
        .filter(_models.Password.id == password_id)
        .first()
    )
    db_password.name = password.name
    db_password.value = password.value

    db.commit()
    db.refresh(db_password)
    return db_password
