from app.db.session import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, ForeignKey, func
from typing import Optional
from enum import Enum
from datetime import datetime, date
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy import String


class UserRole(Enum):
    VIEWER = "viewer"
    MANAGER = "manager"
    HR = "hr_admin"


class EmploymentType(Enum):
    FULLTIME = "full_time"
    PARTTIME = "parttime"
    CONTRACTOR = "contractor"
    INTER = "intern"

class Action(Enum):
    READ = "read"
    UPDATE = "update"
    DELETE = "delete"


class Department(Enum):
    ENGINEERING = "engineering"
    SALES = "sales"
    MARKETING = "marketing"
    FINANCE = "finance"
    HR = "hr"
    SUPPORT = "support"
    OPERATIONS = "operations"

class Grade(Enum):
    JUNIOR = "junior"
    MIDDLE = "middle"
    SENIOR = "senior"
    LEAD = "lead"
    PRINCIPAL = "principal"

class RecordType(Enum):
    NDA = "nda"
    BACKGROUNDCHECK = "background_check"
    CERTIFICATION = "certification"
    VISA = "visa"

class Status(Enum):
    PENDING = "pending"
    VALID = "valid"
    EXPIRED = "expired"


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[UserRole] = mapped_column(nullable=False)

    person: Mapped[Optional["Person"]] = relationship(back_populates="user")

    person_id: Mapped[int | None] = mapped_column(ForeignKey("persons.id", ondelete="SET NULL"))

    is_active: Mapped[bool] = mapped_column(default=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now(), index=True)


class Person(Base):
    __tablename__ = "persons"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    first_name: Mapped[str] = mapped_column(String(50), nullable=False)
    last_name: Mapped[str] = mapped_column(String(255), nullable=False)
    work_email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    phone: Mapped[int] = mapped_column(Integer, unique=True, nullable=False )
    photo_url: Mapped[str] = mapped_column(String(1024), nullable=False)
    status: Mapped[str] = mapped_column(String(50), default="active")

    user: Mapped[Optional["User"]] = relationship(back_populates="person")

    date_of_birth: Mapped[date] = mapped_column(nullable=False)
    home_adress: Mapped[str] = mapped_column(nullable=False)
    national_id: Mapped[int] = mapped_column(nullable=False)


    created_at: Mapped[datetime] = mapped_column(server_default=func.now(), index=True)
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), index=True)


class AuditLog(Base):
    __tablename__ = "auditlog"


    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    actor_user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))

    person_id: Mapped[int] = mapped_column(ForeignKey("persons.id", ondelete="CASCADE"))

    field_name: Mapped[list[str]] = mapped_column(ARRAY(String), nullable=False)
    action: Mapped[Action] = mapped_column(nullable=False)
    ip_adress: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now(), index=True)





class Employment(Base):
    __tablename__ = "employments"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    person_id: Mapped[int] = mapped_column(ForeignKey("persons.id", ondelete="CASCADE"))

    job_title: Mapped[str] = mapped_column(String(128), nullable=False)
    department: Mapped[Department] = mapped_column(nullable=False)

    manager_id: Mapped[int] = mapped_column(ForeignKey("persons.id"))

    start_date: Mapped[datetime] = mapped_column(nullable=False)
    end_date: Mapped[datetime] = mapped_column(nullable=True)

    is_current: Mapped[bool] = mapped_column(default=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now(), index=True)

    salary: Mapped[float] = mapped_column()
    currency: Mapped[str] = mapped_column(String(3), nullable=False)



class Classification(Base):
    __tablename__ = "classifications"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    person_id: Mapped[int] = mapped_column(ForeignKey("persons.id"))
    employment_type: Mapped[EmploymentType] = mapped_column(nullable=False)
    grade: Mapped[Grade] = mapped_column(nullable=False)
    is_exempt: Mapped[bool]
    effective_from: Mapped[datetime] = mapped_column(server_default=func.now(), index=True)
    effective_to: Mapped[datetime] = mapped_column(nullable=True)

    created_at: Mapped[datetime] = mapped_column(server_default=func.now(), index=True)


class CompilianceRecord(Base):
    __tablename__ = "compiliancerecords"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    person_id: Mapped[int] = mapped_column(ForeignKey("persons.id"))
    record_type: Mapped[RecordType] = mapped_column(nullable=False)
    status: Mapped[Status] = mapped_column(nullable=False)
    issued_date: Mapped[datetime] = mapped_column(nullable=False)
    expires_date: Mapped[datetime] = mapped_column(nullable=False)
    notes: Mapped[str | None]
    created_at: Mapped[datetime] = mapped_column(server_default=func.now(), index=True)
    document_url:  Mapped[str | None]
