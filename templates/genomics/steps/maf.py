from sofia_.step import Resource, Step
from lhc.io.maf_.index import IndexedMafFile
from lhc.io.vcf_.iterator import Variant


try:
    import pysam

    class MafSet(Resource):
        """A set of variants parsed from a .vcf file
        """

        EXT = {'.maf', '.maf.gz'}
        FORMAT = 'maf_file'
        OUT = ['maf_set']

        def get_interface(self, filename):
            return IndexedMafFile(filename, pysam.TabixFile(filename))

    class GetMafByVariant(Step):

        IN = ['maf_set', 'variant']
        OUT = ['maf']

        def calculate(self, maf_set, variant):
            #TODO: check matched variants
            if variant is None:
                return None
            try:
                overlap = maf_set.fetch(variant.chr, variant.pos, variant.pos + 1)
            except ValueError:
                return None
            hits = [o for o in overlap if o.start_position == variant.pos and
                    o.reference_allele == variant.ref and variant.alt in {o.tumour_seq_allele1, o.tumour_seq_allele2}]
            if len(hits) == 0:
                return None
            return hits

    class ConvertMafToVariant(Step):

        IN = ['maf']
        OUT = ['variant']

        def calculate(self, maf):
            if maf is None:
                return None
            if isinstance(maf, list):
                return [
                    Variant(m.chromosome,
                           m.start_position,
                           '.', m.reference_allele,
                           ','.join({m.tumour_seq_allele1, m.tumour_seq_allele2} - {m.reference_allele}),
                           m.score,
                           '.')
                for m in maf]
            return Variant(maf.chromosome,
                           maf.start_position,
                           '.', maf.reference_allele,
                           ','.join({maf.tumour_seq_allele1, maf.tumour_seq_allele2} - {maf.reference_allele}),
                           maf.score,
                           '.')

except ImportError:
    import sys
    sys.stderr.write('Unable to import pysam. MAF sets are unavailable.')