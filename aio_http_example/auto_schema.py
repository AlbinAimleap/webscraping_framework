from typing import Type, Dict, ClassVar, List, Optional, Any
from sqlalchemy import Column, Integer, String, Boolean, JSON
from sqlalchemy.orm import Session
from pydantic import BaseModel as PydanticBaseModel
from aio_http.core.db import SessionLocal, Base, init_db


created_models: Dict[str, Type[Base]] = {}

class BaseModel(PydanticBaseModel):
    """Base Pydantic model with CRUD methods."""
    id: ClassVar[int] = None
    
    class Config:
        from_attributes = True
        populate_by_name = True
        use_enum_values = True
        validate_assignment = True
        arbitrary_types_allowed = True
        json_encoders = {
            set: list,
            frozenset: list,
            bytes: lambda v: v.decode(),
        }
    
    @classmethod
    def init(cls) -> None:
        """Create the corresponding table in the database."""
        model_class = create_sqlalchemy_model_from_pydantic(cls)
        Base.metadata.create_all(bind=SessionLocal().bind)
        print(f"Table for {cls.__name__} created or already exists.")

    def save(self) -> None:
        """Save the current instance to the database."""
        session = SessionLocal()
        try:
            model_class = create_sqlalchemy_model_from_pydantic(self.__class__)
            model_instance = model_class(**self.dict())
            session.add(model_instance)
            session.commit()
            print(f"Saved to {model_instance.__tablename__}")
        except Exception as e:
            session.rollback()
            print("Error saving instance:", e)
        finally:
            session.close()

    @classmethod
    def get_by_id(cls, id: int) -> Optional["BaseModel"]:
        """Retrieve an instance by its ID."""
        session = SessionLocal()
        try:
            model_class = create_sqlalchemy_model_from_pydantic(cls)
            instance = session.query(model_class).filter(model_class.id == id).first()
            if instance:
                return cls.from_orm(instance) 
            return None
        finally:
            session.close()

    @classmethod
    def update(cls, id: int, **kwargs: Any) -> Optional["BaseModel"]:
        """Update an instance by its ID."""
        session = SessionLocal()
        try:
            model_class = create_sqlalchemy_model_from_pydantic(cls)
            instance = session.query(model_class).filter(model_class.id == id).first()
            if instance:
                for key, value in kwargs.items():
                    setattr(instance, key, value)
                session.commit()
                return cls.from_orm(instance)
            return None
        except Exception as e:
            session.rollback()
            print("Error updating instance:", e)
            return None
        finally:
            session.close()

    @classmethod
    def delete(cls, id: int) -> bool:
        """Delete an instance by its ID."""
        session = SessionLocal()
        try:
            model_class = create_sqlalchemy_model_from_pydantic(cls)
            instance = session.query(model_class).filter(model_class.id == id).first()
            if instance:
                session.delete(instance)
                session.commit()
                print(f"{cls.__name__} with ID {id} deleted.")
                return True
            print(f"{cls.__name__} with ID {id} not found.")
            return False
        except Exception as e:
            session.rollback()
            print("Error deleting instance:", e)
            return False
        finally:
            session.close()

    @classmethod
    def get_all(cls) -> List["BaseModel"]:
        """Retrieve all instances of the model."""
        session = SessionLocal()
        try:
            model_class = create_sqlalchemy_model_from_pydantic(cls)
            instances = session.query(model_class).all()
            return [cls.from_orm(instance) for instance in instances]  # Convert to Pydantic model instances
        finally:
            session.close()

def create_sqlalchemy_model_from_pydantic(pydantic_model: Type[PydanticBaseModel]) -> Type[Base]:
    """Creates an SQLAlchemy model class from a Pydantic model."""
    
    model_class_name = pydantic_model.__name__ + 'Model'
    
    # Check if the model class already exists in the global dictionary
    if model_class_name in created_models:
        return created_models[model_class_name]

    # Define the new model attributes
    attributes = {
        "__tablename__": pydantic_model.__name__.lower(),
        "id": Column(Integer, primary_key=True, autoincrement=True),
    }

    for field_name, field_type in pydantic_model.__annotations__.items():
        if field_name == 'id':
            continue  # Skip the id field, as it's already defined
        
        if field_type == bool:
            column_type = Boolean
        elif field_type == str:
            column_type = String
        elif field_type == int:
            column_type = Integer
        else:
            column_type = JSON

        attributes[field_name] = Column(column_type, nullable=False)

    # Create the model class dynamically and store it in the global dictionary
    model_class = type(model_class_name, (Base,), attributes)
    created_models[model_class_name] = model_class

    return model_class

class User(BaseModel):
    name: str
    age: int


class TestModel(BaseModel):
    name: str
    age: int
    
TestModel.init()


user = TestModel(name="John Doe", age=30)
user.save()

# Retrieve the user by ID
retrieved_user = TestModel.get_by_id(1)
print(retrieved_user)

# Delete the user
# User.delete(1)
