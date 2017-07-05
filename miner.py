import hashlib
from time import sleep


def hash_256(string):
    return hashlib.sha256(string.encode('utf-8')).hexdigest()


class TransactionGenerator:
    def __init__(self):
        self.random_seed = 0

    def generate_transaction(self):
        transaction_payload = 'This is a transaction between A and B. ' \
                              'We add a random seed here {} to make its hash unique'.format(self.random_seed)
        transaction_hash = hash_256(transaction_payload)
        self.random_seed += 1
        return transaction_hash


# a block is a set of transactions and contains information of the previous blocks.
# https://bitcoin.stackexchange.com/questions/8031/what-are-bitcoin-miners-really-solving
class Block:
    def __init__(self, hash_prev_block, target):
        self.transactions = []
        self.hash_prev_block = hash_prev_block  # hash of the all previous blocks. used to maintain integrity.
        self.hash_merkle_block = None
        self.target = target
        self.nounce = 0

    def add_transaction(self, new_transac):
        if not self.is_block_full():
            self.transactions.append(new_transac)
            self.hash_merkle_block = hash_256(str('-'.join(self.transactions)))

    def is_block_full(self):
        # blocks cannot go above 1Mb. Here let's say we cannot go above 1000 transactions.
        return len(self.transactions) >= 1000

    def is_block_ready_to_mine(self):
        return self.is_block_full()

    def __str__(self):
        return '-'.join([self.hash_merkle_block, str(self.nounce)])

    def apply_mining_step(self):
        current_block_hash = hash_256(self.__str__())
        print('CURRENT_BLOCK_HASH = {}, TARGET = {}'.format(current_block_hash, self.target))
        if int(current_block_hash, 16) < int(self.target, 16):
            print('Block was successfully mined! You will get a reward of x BTC!')
            print('It took {} steps to mine it.'.format(self.nounce))
            return True
        else:
            # Incrementing the nounce to change current_block_hash to hope to be below the target.
            self.nounce += 1
        return False


class BlockChain:
    def __init__(self):
        self.block_chain = []

    def push(self, block):
        self.block_chain.append(block)

    def notify_everybody(self):
        print('-' * 80)
        print('TO ALL THE NODES OF THE NETWORK, THIS BLOCK HAS BEEN ADDED:')
        print('[block #{}] : {}'.format(len(self.block_chain), self.get_last_block()))
        print('-' * 80)

    def get_last_block(self):
        return self.block_chain[-1]


def my_first_miner():
    last_block_header = '0e0fb2e3ae9bd2a0fa8b6999bfe6ab7df197a494d4a02885783a697ac74940d9'
    last_block_target = '000ddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd'

    # init the block chains
    block_chain = BlockChain()

    transaction_generator = TransactionGenerator()

    # fills a block with transactions. We have 1500 pending transactions.
    # Sorry 500 transactions will have to wait for the next block!
    block = Block(last_block_header, last_block_target)
    for i in range(1500):
        block.add_transaction(transaction_generator.generate_transaction())

    assert block.is_block_full()
    assert block.is_block_ready_to_mine()

    # now that our block is full, we can start to mine it.
    while not block.apply_mining_step():
        continue

    block_chain.push(block)
    block_chain.notify_everybody()
    sleep(5)

    # Difficulty is updated every 2016 blocks.
    # Objective is one block generated every 10 minutes.
    # If during the last two weeks, blocks are generated every 5 minutes, then difficulty is multiplied by 2.
    last_block_header = hash_256(str(block_chain.get_last_block()))

    block_2 = Block(last_block_header, last_block_target)

    for i in range(1232):
        block_2.add_transaction(transaction_generator.generate_transaction())

    assert block_2.is_block_full()
    assert block_2.is_block_ready_to_mine()

    # now that our block is full, we can start to mine it.
    while not block_2.apply_mining_step():
        continue

    block_chain.push(block_2)
    block_chain.notify_everybody()
    sleep(5)

    # now let's increase the difficulty.
    # we have now 4 zeros at the beginning instead of 3.
    last_block_target = '0000dddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd'

    last_block_header = hash_256(str(block_chain.get_last_block()))

    block_3 = Block(last_block_header, last_block_target)

    for i in range(1876):
        block_3.add_transaction(transaction_generator.generate_transaction())

    assert block_3.is_block_full()
    assert block_3.is_block_ready_to_mine()

    # now that our block is full, we can start to mine it.
    while not block_3.apply_mining_step():
        continue

    block_chain.push(block_3)
    block_chain.notify_everybody()
    sleep(5)

    print('')
    print('SUMMARY')
    print('')
    for i, block_added in enumerate(block_chain.block_chain):
        print('Block #{} was added. It took {} steps to find it.'.format(i, block_added.nounce))
    print('Difficulty was increased for the last block!')


if __name__ == '__main__':
    my_first_miner()
