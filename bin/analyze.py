#!/usr/bin/env python

import logging
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
from vasptools import read, hasdirs
from vasptools.report import Report
from vasptools.analysis import generate_report

logger = logging.getLogger('log')


def get_args(argv=''):
    """
    Parses arguments from command line
    :param argv: arguments to be parsed
    :return: Namespace parsed arguments
    """
    options = dict(description='',
                   formatter_class=ArgumentDefaultsHelpFormatter)

    parser = ArgumentParser(**options)

    parser.add_argument('directory', nargs='?', default='.',
                        help='directory on which to run the code')

    parser.add_argument('-n', '--name', dest='filename', default='vasprun.xml',
                        help='name of the .xml file to be read')
    parser.add_argument('-i', '--ignore', default=[],
                        help='list of directory names to ignore from analysis')
    choices = ['ni', 'ne', 'F', 'E0', 'dE', 'T', 'E', 'm', 'time']
    parser.add_argument('--rep', '--report', nargs='*', dest='reps',
                        choices=choices,
                        help='list of results to report')

    parser.add_argument('--ads')
    parser.add_argument('--surf_en')
    parser.add_argument('--sd', '--subdir', '--sub-directory', dest='subdir', default='',
                        help='name of the subdirectory on which to do the analysis')

    if argv:
        if isinstance(argv, str):
            argv = argv.split()
        elif not hasattr(argv, '__iter__'):
            raise TypeError(f'argv must be `str` or iterable, not {type(argv)}')
        args = parser.parse_args(argv)
    else:
        # get arguments from console
        args = parser.parse_args()

    return args


def main(argv=''):
    args = get_args(argv)

    # results = read(**vars(args))
    # report = Report(results, **vars(args))

    results = read(filename=args.filename,
                   directory=args.directory,
                   ignore=args.ignore,
                   subdir=args.subdir)

    report = generate_report(results,
                             ads=args.ads,
                             surf_en=args.surf_en,
                             reps=args.reps,
                             subdir=args.subdir)

    print(report)


if __name__ == '__main__':
    from os import path
    p = path.expanduser('~/OneDrive/Documents/TAMU/structs/PtCu/111/224/vasprun_test/ads_O_0.25_fcc')
    main(f'{p}')
