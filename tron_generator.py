import ecdsa
import base58
import ecdsa
import random

from Crypto.Hash import keccak


def keccak256(data):
    hasher = keccak.new(digest_bits=256)
    hasher.update(data)
    return hasher.digest()


def get_signing_key(raw_priv):
    return ecdsa.SigningKey.from_string(raw_priv, curve=ecdsa.SECP256k1)


def verifying_key_to_addr(key):
    pub_key = key.to_string()
    primitive_addr = b'\x41' + keccak256(pub_key)[-20:]
    # 0 (zero), O (capital o), I (capital i) and l (lower case L)
    addr = base58.b58encode_check(primitive_addr)
    return addr


while True:
    raw = bytes(random.sample(range(0, 256), 32))
    # raw = bytes.fromhex('a0a7acc6256c3..........b9d7ec23e0e01598d152')
    key = get_signing_key(raw)
    addr = verifying_key_to_addr(key.get_verifying_key()).decode()
    print('Address:     ', addr)
    print('Address(hex):', base58.b58decode_check(addr.encode()).hex())
    print('Public Key:  ', key.get_verifying_key().to_string().hex())
    print('Private Key: ', raw.hex())

    break

