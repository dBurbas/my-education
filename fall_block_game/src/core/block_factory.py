from abc import ABC, abstractmethod
from src.core.block import Block
from src.core.exception import BlockFactoryError
import random


class IBlockFactory(ABC):
    """Abstract base class for a block factory."""

    @abstractmethod
    def get_random_block(self) -> Block:
        """Return a random block from the factory's bag.

        :return: A new Block instance.
        :rtype: Block
        """
        pass

    @abstractmethod
    def fill_bag(self):
        """Refill the bag with all block blueprints and shuffle them."""
        pass


class BlockFactory(IBlockFactory):
    """Concrete block factory using a random bag.

    :param block_blueprints: List of dictionaries, each containing block data.
    :type block_blueprints: list[dict]
    """

    def __init__(self, block_blueprints: list[dict]):
        """Initialize the factory with available block blueprints.

        :param block_blueprints: List of block definition dictionaries.
        :type block_blueprints: list[dict]
        :raises BlockFactoryError: If the blueprint list is empty.
        """
        if not block_blueprints:
            raise BlockFactoryError("block_blueprints cannot be empty")
        self._blueprints = block_blueprints
        self._bag: list[dict] = []

    def fill_bag(self) -> None:
        """Fill the bag with a copy of all blueprints and shuffle randomly."""

        self._bag = self._blueprints.copy()
        random.shuffle(self._bag)

    def get_random_block(self) -> Block:
        """Return a random block from the bag, refilling if necessary.

        :return: A new Block instance created from the next blueprint.
        :rtype: Block
        """
        if not self._bag:
            self.fill_bag()

        blueprint = self._bag.pop()
        return Block(block_data=blueprint)
