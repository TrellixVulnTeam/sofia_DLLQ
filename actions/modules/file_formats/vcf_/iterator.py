import gzip

from collections import OrderedDict, namedtuple
from itertools import izip

Variant = namedtuple('Variant', ('chr', 'pos', 'id', 'ref', 'alt', 'qual', 'filter', 'info', 'samples'))


class VcfIterator(object):

    CHR = 0
    POS = 1
    ID = 2
    REF = 3
    ALT = 4
    QUAL = 5
    FILTER = 6
    INFO = 7
    FORMAT = 8
    
    def __init__(self, fname):
        self.fname = fname
        self.fhndl = gzip.open(fname) if fname.endswith('.gz') else open(fname)
        self.line_no = 0
        self.hdrs = self._parse_headers()
        self.samples = self.hdrs['##SAMPLES']
        del self.hdrs['##SAMPLES']
    
    def __del__(self):
        if hasattr(self, 'fhndl') and not self.fhndl.closed:
            self.fhndl.close()
    
    def __iter__(self):
        return self
    
    def next(self):
        self.line_no += 1
        return self._parse_line(self.fhndl.next())
    
    def seek(self, fpos):
        self.fhndl.seek(fpos)
    
    def _parse_headers(self):
        fhndl = self.fhndl
        hdrs = OrderedDict()
        line = fhndl.next().strip()
        self.line_no += 1
        if 'VCF' not in line:
            raise ValueError('Invalid VCF file. Line 1: {}'.format(line.strip()))
        while line.startswith('##'):
            key, value = line.split('=', 1)
            if key not in hdrs:
                hdrs[key] = []
            hdrs[key].append(value)
            line = fhndl.next().strip()
            self.line_no += 1
        hdrs['##SAMPLES'] = line.strip().split('\t')[9:]
        return hdrs
    
    def _parse_line(self, line):
        parts = line.strip().split('\t')
        return Variant(parts[self.CHR],
                       int(parts[self.POS]) - 1,
                       parts[self.ID],
                       parts[self.REF],
                       parts[self.ALT],
                       self._parse_quality(parts[self.QUAL]),
                       parts[self.FILTER],
                       self._parse_attributes(parts[self.INFO]),
                       self._parse_samples(parts))

    def _parse_quality(self, qual):
        if qual == '.':
            return '.'
        try:
            res = float(qual)
        except TypeError:
            return '.'
        return res
    
    def _parse_attributes(self, attr_line):
        return dict(attr.split('=', 1) if '=' in attr else (attr, attr) for attr in attr_line.strip().split(';'))
    
    def _parse_samples(self, parts):
        res = {}
        if self.FORMAT < len(parts):
            keys = parts[self.FORMAT].split(':')
            for i, sample in enumerate(self.samples):
                if parts[self.FORMAT + i + 1] == '.':
                    continue
                res[sample] = dict(izip(keys, parts[self.FORMAT + i + 1].strip().split(':')))
        return res
