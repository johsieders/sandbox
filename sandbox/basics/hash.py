# j.siedersleben
# fasttrack to professional programming
# lesson 2: collections
# 17.11.2020
# 11.05.2025

########################################
##      Handmade Hash Dictionary      ##
########################################

def make_dict():
    """
    This is a simple dictionary based on hashing.
    The list slots contains for each hash value the list of all
    entries sharing that hash value = a slot
    Searching is in two steps:
    1) Get the corresponding slot if any
    2) get the corresponding (k, v)-pair in that slot if any
    :return: get and set functions

    This implementation uses no class.
    The class HashDictionary will be discussed shortly
    """
    slots = []

    def get(key):
        h0 = hash(key)
        for h, slot in slots:
            if h == h0:  # slot found
                for k, v in slot:
                    if k == key:  # key found
                        return v

        raise ValueError(str(key) + ' is not in dict')  # no such key

    def set(key, value):
        h0 = hash(key)
        for h, slot in slots:
            if h == h0:  # found slot
                for i, (k, v) in enumerate(slot):
                    if k == key:  # found key, overwrite (k, v)
                        slot[i] = (key, value)
                        return
                # no such key in slot
                slot.append((key, value))
                return

        # no slot matching h0 = hash(key)
        slots.append((h0, [(key, value)]))

    return get, set


## The same algorithms wrapped in a class
## __getitem__ overloads v = map[k]
## __setitem__ overloads map[k] = v

class Hashdict(object):
    def __init__(self):
        self.slots = []

    def __getitem__(self, key):
        h0 = hash(key)
        for h, slot in self.slots:
            if h == h0:  # slot found
                for k, v in slot:
                    if k == key:  # key found
                        return v

        raise ValueError(str(key) + ' is not in dict')  # no such key

    def __setitem__(self, key, value):
        h0 = hash(key)
        for h, slot in self.slots:
            if h == h0:  # found slot
                for i, (k, v) in enumerate(slot):
                    if k == key:  # found key, overwrite (k, v)
                        slot[i] = (key, value)
                        return
                # no such key in slot
                slot.append((key, value))
                return

        # no slot matching h0 = hash(key)
        self.slots.append((h0, [(key, value)]))
