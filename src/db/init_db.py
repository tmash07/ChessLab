from .base import Base
from .database import engine
from . import models


def initialize_database() -> None:
    Base.metadata.create_all(engine)


if __name__ == "__main__":
    initialize_database()