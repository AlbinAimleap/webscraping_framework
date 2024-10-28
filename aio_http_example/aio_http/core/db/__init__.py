from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from typing import TypeVar, Generic, List, Optional
from aio_http.core.db.config import DATABASE_URL

ModelType = TypeVar('ModelType', bound='BaseModel')

engine = create_engine(DATABASE_URL)
Base = declarative_base()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class BaseModel(Base):
    """Base model class for all database models."""
    
    __abstract__ = True

    def save(self) -> None:
        """Save the instance to the database."""
        session: Session = SessionLocal()
        try:
            session.add(self)
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    @classmethod
    def get(cls: TypeVar('T', bound='BaseModel'), id: int) -> Optional[ModelType]:
        """Retrieve a model instance by its ID.

        Args:
            id (int): The ID of the instance to retrieve.

        Returns:
            Optional[ModelType]: The instance if found, otherwise None.
        """
        session: Session = SessionLocal()
        try:
            return session.query(cls).filter(cls.id == id).one_or_none()
        finally:
            session.close()

    @classmethod
    def get_all(cls: TypeVar('T', bound='BaseModel')) -> List[ModelType]:
        """Retrieve all instances of the model.

        Returns:
            List[ModelType]: A list of all instances.
        """
        session: Session = SessionLocal()
        try:
            return session.query(cls).all()
        finally:
            session.close()

    def update(self, **kwargs) -> None:
        """Update the model instance with the given keyword arguments.

        Args:
            **kwargs: The fields to update with their new values.
        """
        session: Session = SessionLocal()
        try:
            for key, value in kwargs.items():
                setattr(self, key, value)
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def delete(self) -> None:
        """Delete the model instance from the database."""
        session: Session = SessionLocal()
        try:
            session.delete(self)
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

def get_db() -> Session:
    """Dependency that provides a database session.

    Yields:
        Session: A SQLAlchemy session for database operations.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db(model=None) -> None:
    """Initialize the database by creating all tables."""
    if model:
        model.__table__.create(bind=engine)
    else:
        Base.metadata.create_all(bind=engine)
