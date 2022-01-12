#!/usr/bin/env python3
# Note: requires at least Python 3.2

import sys
import argparse
import csv
import logging
import json
import re

logger = logging.getLogger(__name__)


def get_dialect(f):
    """ Get CSV dialect from file. """
    sniffer = csv.Sniffer()

    dialect = sniffer.sniff(f.read(8192))
    f.seek(0)

    return dialect


def get_header(f):
    """ Return CSV header for file f. """

    reader = csv.reader(f, get_dialect(f))

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


def analyse_fields(files):
    """ Return all and common fields for CSV files. """
    logger.info('Analysing fields for %s files.', len(files))

    common_fields = set()
    all_fields = set()
    for f in files:
        try:
            fields = get_header(f)
        except:
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

    return all_fields, common_fields


def json_fields(all_fields, common_fields):
    """ Return JSON with field analysis. """

    output = dict(
        all_fields=all_fields,
        common_fields=common_fields
    )

    print(json.dumps(output, indent=2))


def merge(files, fieldnames, outfile, extra_fields=None):
    """
    Merge CSV files.

    Takes extra_fields function with file argument to add extra fields
    (e.g. based on filename). Results override CSV.
    """
    logger.info('Merging %d CSV-files into %s', len(files), outfile.name)

    writer = csv.DictWriter(outfile, fieldnames=fieldnames)

    writer.writeheader()

    count = 0
    for f in files:
        logger.info('Merging: %s', f.name)

        try:
            dialect = get_dialect(f)
        except:
            logger.exception('Error retreiving dialect from file %s', f.name)
            raise

        reader = csv.DictReader(f, fieldnames, dialect=dialect)

        # Skip header, but check if all fields are in there
        header = set(next(reader).values())
        if not header.issubset(fieldnames):
            additional_fields = header.difference(fieldnames)

            logger.warning(
                "Warning: %d unkown field(s) detected: %s",
                len(additional_fields), additional_fields
            )

        for item in reader:
            if extra_fields:
                item.update(extra_fields(f))

            writer.writerow(item)
            count += 1

        logger.info('%d records written', count)

    outfile.close()


def main():
    """ Read and parse field headers of CSV. """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        'operation',
        metavar='operation', choices=['json_fields', 'merge']
    )
    parser.add_argument('files', nargs='+', type=argparse.FileType('r'))
    parser.add_argument(
        '--logging', '-l', help='Log level.', type=str,
        default='info', choices=('debug', 'info', 'warn', 'error')
    )
    parser.add_argument(
        '--output', '-o', help='Merge output', type=argparse.FileType('w'),
        default='merged.csv'
    )
    parser.add_argument(
        '--extra-fields', '-e',
        help='Extra fields (Python statement with re allowed).',
        type=lambda code: eval(code, dict(re=re))
    )

    args = parser.parse_args()

    setup_logging(args.logging.upper())

    all_fields, common_fields = analyse_fields(args.files)

    logger.info('All fields: %s', join_fields(all_fields))
    logger.info('Common fields: %s', join_fields(common_fields))

    if args.operation == 'json_fields':
        json_fields(all_fields, common_fields)
    elif args.operation == 'merge':
        merge(
            args.files, all_fields, args.output,
            extra_fields=args.extra_fields
        )

    for f in args.files:
        f.close()

if __name__ == "__main__":
    main()
