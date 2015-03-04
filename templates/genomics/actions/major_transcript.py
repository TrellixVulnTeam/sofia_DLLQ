from sofia_.action import Action
from warnings import warn


class GetMajorTranscriptCodingSequence(Action):
    """
    Get the coding sequence of the major transcript.
    """

    IN = ['chromosome_sequence_set', 'major_transcript']
    OUT = ['coding_sequence']

    def calculate(self, chromosome_sequence_set, major_transcript):
        if major_transcript is None:
            return None
        res = major_transcript.get_sub_seq(chromosome_sequence_set, types={'CDS'})
        if len(res) % 3 != 0:
            warn('{} coding sequence length not a multiple of 3, possible mis-annotation'.format(major_transcript.name))
            #return None
        return res


class GetFivePrimeUtr(Action):
    """
    Get the 5' untranslated region of the major transcript.
    """

    IN = ['chromosome_sequence_set', 'major_transcript']
    OUT = ['five_prime_utr']

    def calculate(self, chromosome_sequence_set, major_transcript):
        if major_transcript is None:
            return None
        return major_transcript.get_sub_seq(chromosome_sequence_set, type="5'UTR5")


class GetThreePrimeUtr(Action):
    """
    Get the 3' untranslated region of the major transcript.
    """

    IN = ['chromosome_sequence_set', 'major_transcript']
    OUT = ['three_prime_utr']

    def calculate(self, chromosome_sequence_set, major_transcript):
        if major_transcript is None:
            return None
        return major_transcript.get_sub_seq(chromosome_sequence_set, type="3'UTR")