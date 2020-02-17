from hashlib import sha256


def getRandomHash():
    with open("/dev/urandom", "rb") as dev_random:
        return sha256(dev_random.read(16)).hexdigest()


def saltWord(word, salt):
    return sha256(word + salt).hexdigest()
