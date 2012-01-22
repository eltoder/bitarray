"""
Demonstrates the implementation of a Bloom filter, see:
http://en.wikipedia.org/wiki/Bloom_filter
"""
import hashlib
from math import exp, log

from bitarray import bitarray


class BloomFilter(object):

    def __init__(self, m, k):
        self.m = m
        self.k = k
        self.array = bitarray(m)
        self.array.setall(0)

    def add(self, key):
        for i in self._hashes(key):
            self.array[i] = 1

    def contains(self, key):
        return all(self.array[i] for i in self._hashes(key))

    def _hashes(self, key):
        """
        generate k different hashes (in the range 0 to m) based on the key
        """
        x = long(hashlib.sha512(str(key)).hexdigest(), 16)
        for _ in xrange(self.k):
            x, y = divmod(x, self.m)
            yield y


def test_bloom(m, k, n):
    b = BloomFilter(m, k)
    for i in xrange(n):
        b.add(i)
        assert b.contains(i)

    p = (1.0 - exp(-k * (n + 0.5) / (m - 1))) ** k
    print 100.0 * p, '%'

    N = 10000
    false_pos = sum(b.contains(i) for i in xrange(n, n + N))
    print 100.0 * false_pos / N, '%'


if __name__ == '__main__':
    test_bloom(10000, 6, 1000)