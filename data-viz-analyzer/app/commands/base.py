from abc import ABC, abstractmethod
from typing import Any


class BaseCommand(ABC):
    @abstractmethod
    def run(self) -> Any:
        """
        :raises: CommandException
        """

    @abstractmethod
    def validate(self) -> None:
        """
        :raises: CommandException
        """
