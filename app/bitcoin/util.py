from pycoin.key import Key


def generate_address_from_xpub(xpub, index=0, is_hardened=False):
    key = Key.from_text(xpub)
    return str(key.subkey(index, is_hardened).address())
