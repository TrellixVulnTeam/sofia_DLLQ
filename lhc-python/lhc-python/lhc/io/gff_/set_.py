from lhc.indices import Index, ExactKeyIndex, OverlappingIntervalIndex
from lhc.interval import Interval


class GffSet(object):
    def __init__(self, iterator):
        self.key_index = ExactKeyIndex()
        self.ivl_index = Index((ExactKeyIndex, OverlappingIntervalIndex))
        self.data = list(iterator)
        for i, entry in enumerate(self.data):
            self.key_index[entry.name] = i
            self.ivl_index[(entry.ivl.chr, entry.ivl)] = i

    def __getitem__(self, key):
        return self.data[self.key_index[key]]
    
    def fetch(self, chr, start, stop):
        return [self.data[v] for k, v in self.ivl_index[chr, Interval(start, stop)]]
