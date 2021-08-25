"""Crypto Hash"""

import hashlib
import json


def crypto_hash(*args):
    """Return a SHA256 hash of given arguments."""

    stringfied_args = sorted(map(json.dumps, args))
    joined_data = "".join(stringfied_args)

    return hashlib.sha256(joined_data.encode("utf-8")).hexdigest()


def main():
    """main"""
    print("Crypto Hash: {}".format(crypto_hash("one", 2, [3])))
    print("Crypto Hash: {}".format(crypto_hash(2, "one", [3])))


if __name__ == "__main__":
    main()
