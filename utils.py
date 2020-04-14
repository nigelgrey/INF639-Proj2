import collections

ClientData = collections.namedtuple('ClientData', ['username','password'])
HashData = collections.namedtuple('HashData', ['xored','password'])
