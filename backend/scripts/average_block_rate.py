"""Block"""

import time

from backend.blockchain.blockchain import Blockchain
from backend.config import SECONDS

blockchain = Blockchain()

times = []
for i in range(1000):
    start_time = time.time_ns()
    blockchain.add_block(i)
    end_time = time.time_ns()

    time_to_mine = (end_time - start_time) / SECONDS
    times.append(time_to_mine)

    average_time = sum(times) / len(times)

    print("New block difficulty {} \n".format(blockchain.chain[-1].difficulty))
    print("Time to mine new block {}s \n".format(time_to_mine))
    print("Average time to add blocks {}s \n".format(average_time))
    print("Current hash {}s \n".format(blockchain.chain[i].current_hash))
