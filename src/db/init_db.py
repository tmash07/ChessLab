from .base import Base
from . import models


def initialize_database(engine) -> None:
    Base.metadata.create_all(engine)


if __name__ == "__main__":
    from .database import engine
    initialize_database(engine)