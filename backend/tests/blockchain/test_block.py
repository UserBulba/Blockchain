"""Block test"""
import time

import pytest
from backend.blockchain.block import GENESIS_DATA, Block
from backend.config import MINE_RATE, SECONDS
from backend.util.hex_to_binary import hex_to_binary as convert


def test_mine_hash():
    """?"""
    last_block = Block.genesis()
    data = "test-data"
    block = Block.mine_block(last_block, data)

    assert isinstance(block, Block)
    assert block.data == data
    assert block.last_hash == last_block.current_hash
    assert convert(block.current_hash)[0:block.difficulty] == "0" * block.difficulty  # noqa: E501


def test_genegis():
    """?"""
    genesis = Block.genesis()

    assert isinstance(genesis, Block)
    for key, value in GENESIS_DATA.items():
        assert getattr(genesis, key) == value


def test_quickly_mined_block():
    """?"""
    last_block = Block.mine_block(Block.genesis(), "foo")
    mined_block = Block.mine_block(last_block, "bar")

    assert mined_block.difficulty == last_block.difficulty + 1


def test_slowly_mined_block():
    """?"""
    last_block = Block.mine_block(Block.genesis(), "foo")
    time.sleep(MINE_RATE / SECONDS)
    mined_block = Block.mine_block(last_block, "bar")

    assert mined_block.difficulty == last_block.difficulty - 1


def test_mined_block_difficulty_limits_at_1():
    """?"""
    last_block = Block(
        time.time_ns(),
        'test_last_hash',
        'test_hash',
        'test_data',
        1,
        0
    )

    time.sleep(MINE_RATE / SECONDS)
    mined_block = Block.mine_block(last_block, 'bar')

    assert mined_block.difficulty == 1

 
@pytest.fixture
def last_block():
    """?"""
    return Block.genesis()


@pytest.fixture
def block(last_block):
    """?"""
    return Block.mine_block(last_block, "test_data")


def test_is_valid_block(last_block, block):
    """?"""
    Block.valid_block(last_block, block)


def test_is_valid_block_bad_last_hash(last_block, block):
    """?"""
    block.last_hash = "evil_last_hash"

    with pytest.raises(Exception,
                       match="last_hash must be correct"):
        Block.valid_block(last_block, block)


def test_is_valid_block_bad_proof_of_work(last_block, block):
    """?"""
    block.current_hash = "fff"

    with pytest.raises(Exception,
                       match="The proof of work requirement is was not met"):  # noqa: E501
        Block.valid_block(last_block, block)


def test_is_valid_block_jumped_difficulty(last_block, block):
    """?"""
    jumped_difficulty = 10
    block.difficulty = jumped_difficulty
    block.current_hash = "{}1234abcd".format("0" * jumped_difficulty)

    with pytest.raises(Exception,
                       match="The block difficulty must only adjust by 1"):  # noqa: E501
        Block.valid_block(last_block, block)


def test_is_valid_block_bad_block_hash(last_block, block):
    """?"""
    block.current_hash = "0000000000000aaabbb"

    with pytest.raises(Exception,
                       match="The block hash must be correct"):  # noqa: E501
        Block.valid_block(last_block, block)
