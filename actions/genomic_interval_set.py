from sofia_.action import Action


class GetIntervalByPosition(Action):
    
    IN = ['genomic_interval_set', 'genomic_position']
    OUT = ['genomic_interval']

    def calculate(self, genomic_interval_set, genomic_position):
        intervals = genomic_interval_set.get_intervals_at_position(
            genomic_position['chromosome_id'],
            genomic_position['chromosome_pos'])
        return [{
            'chromosome_id': interval.chr,
            'start': interval.start,
            'stop': interval.stop,
            'interval_name': interval.name,
        } for interval in intervals]
    
    def format(self, genomic_interval):
        return genomic_interval['data'].name


class GetBoundsProximity(Action):

    IN = ['genomic_position', 'genomic_interval']
    OUT = ['bounds_proximity']

    def calculate(self, genomic_position, genomic_interval):
        if genomic_position is None or len(genomic_interval) == 0:
            return None
        ds = []
        for interval in genomic_interval:
            ds.append((genomic_position['chromosome_pos'] - interval['start'], '5p'))
            ds.append((genomic_position['chromosome_pos'] - interval['stop'], '3p'))
        d = sorted(ds, key=lambda x:abs(x[0]))[0]
        return '{}{:+d}'.format(d[1], d[0])
