import argparse

from lhc.filetools.flexible_opener import open_flexibly


class OpenReadableFile(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        if values is None:
            from sys import stdin as fhndl
        elif isinstance(values, list):
            fhndl = [open_flexibly(value)[1] for value in values]
        else:
            fname, fhndl = open_flexibly(values)
        setattr(namespace, self.dest, fhndl)