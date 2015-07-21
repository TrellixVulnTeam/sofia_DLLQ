from sofia_.step import Step
from lhc.binf.genomic_coordinate import GenomicInterval


class ConvertPositionToInterval(Step):

    IN = ['genomic_position']
    OUT = ['genomic_interval']

    def calculate(self, genomic_position):
        return GenomicInterval(genomic_position.chr, genomic_position.pos, genomic_position.pos + 1)
