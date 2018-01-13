#!/usr/bin/env python3

import sys
import argparse
import csv
import logging
import json

logger = logging.getLogger(__name__)


def get_header(f):
    """ Return CSV header for file f. """

    # Sniff csv dialect
    dialect = csv.Sniffer().sniff(f.read(8192))
    f.seek(0)

    reader = csv.reader(f, dialect)

    # Read first row
    return next(reader)


def join_fields(fields):
    """ Join fields with ', ' for display. """

    return ', '.join(fields)


def setup_logging(log_level):
    # Setup logging
    stderr = logging.StreamHandler(sys.stderr)
    logger.addHandler(stderr)

    numeric_level = getattr(logging, log_level)
    logger.setLevel(numeric_level)


def sort_list(i):
    """ Return iterable as sorted list. """
    l = list(i)
    l.sort()

    return l


def main():
    """ Read and parse field headers of CSV. """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('files', nargs='+', type=argparse.FileType('r'))
    parser.add_argument(
        '--logging', '-l', help='Log level.', type=str,
        default='info', choices=('debug', 'info', 'warn', 'error')
    )

    args = parser.parse_args()

    setup_logging(args.logging.upper())

    logger.debug('Analysing fields for %s files.\n', len(args.files))

    common_fields = set()
    all_fields = set()
    for f in args.files:
        try:
            fields = get_header(f)
        except csv.Error:
            logger.exception('Error retreiving header from file %s', f.name)
            raise

        logger.debug('%s: %s', f.name, join_fields(fields))

        # From now on, we work with sets
        fields = set(fields)

        all_fields |= fields

        # Initiate on first iteration
        if not common_fields:
            common_fields = set(fields)
        else:
            common_fields &= fields

    all_fields = sort_list(all_fields)
    common_fields = sort_list(common_fields)

    logger.info('All fields: %s', join_fields(all_fields))
    logger.info('Common fields: %s', join_fields(common_fields))

    output = dict(
        all_fields=all_fields,
        common_fields=common_fields
    )

    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
