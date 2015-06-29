import os
import tempfile
import unittest

from collections import namedtuple
from lhc.io.txt_ import Iterator, Set, Entity, Column
from lhc.indices import CompoundIndex, KeyIndex, IntervalIndex
from lhc.interval import Interval


class TestSet(unittest.TestCase):
    def setUp(self):
        self.data = [('1', '10', '20', 'a'),
                     ('1', '30', '60', 'b'),
                     ('1', '100', '110', 'c'),
                     ('2', '15', '30', 'd'),
                     ('2', '40', '50', 'e'),
                     ('3', '10', '110', 'f')]
        fhndl, self.fname = tempfile.mkstemp()
        os.write(fhndl, '\n'.join('\t'.join(row) for row in self.data))
        os.close(fhndl)

    def test_set(self):
        columns = [Column(str, i) for i in xrange(4)]
        entity_factory = Entity(namedtuple('Entry', ['V1', 'V2', 'V3', 'V4']), columns)
        it = Iterator(open(self.fname), entity_factory)
        index = CompoundIndex(KeyIndex, IntervalIndex)
        data = Set(it, index, key=lambda x: (x.V1, Interval(int(x.V2), int(x.V3))))

        self.assertEquals(self.data[0], tuple(data[('1', Interval(0, 15))][0]))


if __name__ == '__main__':
    unittest.main()