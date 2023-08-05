import sqlalchemy as _sql
import sqlalchemy.orm as _orm
from database import Base


class User(Base):
    __tablename__ = "users"
    id: int = _sql.Column(_sql.Integer, primary_key=True, index=True)
    email: str = _sql.Column(_sql.String, unique=True, index=True)
    hashed_password: str = _sql.Column(_sql.String)
    tfa: bool = _sql.Column(_sql.Boolean, default=False)
    tfa_secret: str = _sql.Column(_sql.String, nullable=True)
    passwords = _orm.relationship("Password", back_populates="owner")


class Password(Base):
    __tablename__ = "passwords"
    id: int = _sql.Column(_sql.Integer, primary_key=True, index=True)
    name: str = _sql.Column(_sql.String, index=True)
    value: str = _sql.Column(_sql.String)
    owner_id: int = _sql.Column(_sql.Integer, _sql.ForeignKey("users.id"))
    owner = _orm.relationship("User", back_populates="passwords")
