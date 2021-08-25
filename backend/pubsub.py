'''PubNub file'''
import os
import time

from pubnub.callbacks import SubscribeCallback
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub
from python_settings import settings

from backend.blockchain.block import Block

os.environ["SETTINGS_MODULE"] = 'settings'

pnconfig = PNConfiguration()
pnconfig.subscribe_key = settings.SUBSCRIBE_KEY
pnconfig.publish_key = settings.PUBLISH_KEY
pubnub = PubNub(pnconfig)

CHANNELS = {
    "TEST": "TEST",
    "BLOCK": "BLOCK"
}


class Listener(SubscribeCallback):
    """Listener class"""
    def __init__(self, blockchain):
        """Initialize"""
        self.blockchain = blockchain

    def message(self, pubnub, message_object):
        """Message"""
        print("\n Channel: {} | Message: {}".format(message_object.channel, message_object.message))  # noqa: E501

        if message_object.channel == CHANNELS["BLOCK"]:
            block = Block.from_json(message_object.message)
            potential_chain = self.blockchain.chain[:]
            potential_chain.append(block)

            try:
                self.blockchain.replace_chain(potential_chain)
                print("\n -- Successfully replaced local chain")
            except Exception as error:  # pylint: disable=broad-except
                print("\n -- Did not replace a chain : {}".format(error))


class PubSub():
    """
    Handles the publish/subscribe layer of the application.
    Provides communication between the nodes of the blockchain network.
    """

    def __init__(self, blockchain):
        """Init"""
        self.pubnub = PubNub(pnconfig)
        self.pubnub.subscribe().channels(CHANNELS.values()).execute()
        self.pubnub.add_listener(Listener(blockchain))

    def publish(self, channel, message):
        """Publish the message object to the channel."""
        self.pubnub.publish().channel(channel).message(message).sync()

    def broadcast_block(self, block):
        """Broadcast a block object to all nodes."""
        self.publish(CHANNELS["BLOCK"], block.to_json())


def main():
    """Main"""
    pubsub = PubSub()

    time.sleep(1)
    pubsub.publish(CHANNELS["TEST"], {"foo": "bar"})


if __name__ == "__main__":
    main()
