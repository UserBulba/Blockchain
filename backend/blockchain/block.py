"""Block"""
import time  # Time module.

from backend.config import MINE_RATE
from backend.util.crypto_hash import crypto_hash as crypto
from backend.util.hex_to_binary import hex_to_binary as convert

GENESIS_DATA = {
    "timestamp": 1,
    "last_hash": "genesis_last_hash",
    "current_hash": "genesis_hash",
    "data": [],
    "difficulty": 3,
    "nonce": "genesis_nonce"
}


class Block:
    """Block: a unit of storage."""

    def __init__(self, timestamp, last_hash,
                 current_hash, data, difficulty, nonce):
        self.timestamp = timestamp
        self.last_hash = last_hash
        self.current_hash = current_hash
        self.data = data
        self.difficulty = difficulty
        self.nonce = nonce

    def __repr__(self):
        return (
            'Block('
            f'timestamp: {self.timestamp}, '
            f'last_hash: {self.last_hash}, '
            f'current_hash: {self.current_hash}, '
            f'data: {self.data}), '
            f'difficulty: {self.difficulty}), '
            f'nonce: {self.nonce})'
        )

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def to_json(self):
        """Serialize the block into a dictionary of its attributes"""
        return self.__dict__

    @staticmethod
    def mine_block(last_block, data):
        """
        Mine a block based on the given last_block and data, until a block hash
        is found that meets the leading 0`s proof of work requirement.
        """
        timestamp = time.time_ns()
        last_hash = last_block.current_hash
        difficulty = Block.adjust_difficulty(last_block, timestamp)
        nonce = 0
        current_hash = crypto(timestamp, last_hash, data, difficulty, nonce)

        while convert(current_hash)[0:difficulty] != '0' * difficulty:

            nonce += 1
            timestamp = time.time_ns()
            difficulty = Block.adjust_difficulty(last_block, timestamp)
            current_hash = crypto(timestamp, last_hash,
                                  data, difficulty, nonce)

            # print(current_hash)
            # print(convert(current_hash)[0:difficulty])

        return Block(timestamp, last_hash, current_hash,
                     data, difficulty, nonce)

    @staticmethod
    def genesis():
        """Generate a genesis block."""
        return Block(**GENESIS_DATA)

    @staticmethod
    def from_json(block_json):
        """Deserialize a block`s json representation back into a block instance."""  # noqa: E501
        return Block(**block_json)

    @staticmethod
    def adjust_difficulty(last_block, new_timestamp):
        """Calculate the adjusted difficulty according to the MINE_RATE"""
        if(new_timestamp - last_block.timestamp) < MINE_RATE:
            return last_block.difficulty + 1

        if (last_block.difficulty - 1) > 0:
            return last_block.difficulty - 1

        return 1

    @staticmethod
    def valid_block(last_block, block):
        """
        Validate a block by enforcing following rules:
            - proper last_hash reference
            - the block must meet the proof of work requirement
            - the difficulty must be adjust by 1
            - the block hash must a valid combination of block fields
        """

        if block.last_hash != last_block.current_hash:
            raise Exception("The block last_hash must be correct")

        if convert(block.current_hash)[0:block.difficulty] != '0' * block.difficulty:  # noqa: E501
            raise Exception("The proof of work requirement is was not met")

        if abs(last_block.difficulty - block.difficulty) > 1:
            raise Exception("The block difficulty must only adjust by 1")

        reconstructed_hash = crypto(
            block.timestamp,
            block.last_hash,
            block.data,
            block.nonce,
            block.difficulty
        )

        if block.current_hash != reconstructed_hash:
            raise Exception("The block hash must be correct")


def main():
    """Main"""
    # genesis_block = Block.genesis()
    # block = Block.mine_block(genesis_block, "Foo")
    # print(block)

    genesis_block = Block.genesis()
    good_block = Block.mine_block(Block.genesis(), "foo")
    # bad_block.last_hash = "evil_data"

    try:
        Block.valid_block(genesis_block, good_block)
    except Exception as error:  # pylint: disable=broad-except
        print("Is valid block {}".format(error))


if __name__ == "__main__":
    main()
