"""Blockchain"""

from backend.blockchain.block import Block


class Blockchain:
    """Blockchain: a public ledger of transactions."""

    def __init__(self):
        self.chain = [Block.genesis()]

    def add_block(self, data):
        """Add block to blockchain"""
        self.chain.append(Block.mine_block(self.chain[-1], data))

    def replace_chain(self, chain):
        """
        Replace the local chain with the
        incoming one if the followint applies:
           - The incoming chain is longer than the local one.
           - The incoming chain is formating properly.
        """

        if len(chain) <= len(self.chain):
            raise Exception("Cannot replace. The incoming chain must be longer.")  # noqa: E501

        try:
            Blockchain.is_valid_chain(chain)
        except Exception as error:
            raise Exception("Cannot replace. The incoming chain is invalid: {}.".format(error)) from None  # noqa: E501

        self.chain = chain

    def to_json(self):
        """Serialize the blockchain into a list of blocks"""
        return list(map(lambda block: block.to_json(), self.chain))

    @staticmethod
    def from_json(chain_json):
        """
        Deserialize a list of serialized blocks into a block chain instance
        The result containt a chain list of Block instances.
        """
        blockchain = Blockchain()
        blockchain.chain = list(map(lambda block_json: Block.from_json(block_json), chain_json))  # noqa: E501

        return blockchain

    @staticmethod
    def is_valid_chain(chain):
        """
        Validate the incoming chain.
        Enforce the following rules of the blockchain:
            - the chain must start with the genesis block
            - block must be formatted correctly
        """

        if chain[0] != Block.genesis():
            raise Exception("The genesis block must be valid")

        for i in range(1, len(chain)):
            block = chain[i]
            last_block = chain[i - 1]

            Block.valid_block(last_block, block)

    def __repr__(self):
        return "Blockchain: {}".format(self.chain)


def main():
    """Main"""
    blockchain = Blockchain()
    blockchain.add_block("one")
    blockchain.add_block("two")
    blockchain.add_block("three")

    print("blockchain.py __name__ {}".format(__name__))
    print(blockchain)


if __name__ == "__main__":
    main()
