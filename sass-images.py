#!/usr/bin/env python

from __future__ import unicode_literals

import argparse
import os
import sass_images

parser = argparse.ArgumentParser(description='Generates inline image information for SASS.')
parser.add_argument('-d', '--dir',
                    default=os.getcwd(),
                    help="Directory from which to read images.")
parser.add_argument('-o', '--output',
                    default='-',
                    type=argparse.FileType('w', 0),
                    help='Output file. Defaults to stdout.')
parser.add_argument('-i', '--inline-threshold',
                    default=2048,
                    type=int,
                    dest='threshold',
                    help='Inline images if less than this many bytes. Default 2048.')
parser.add_argument('-u', '--url-prefix',
                    default='',
                    dest='prefix',
                    help='Prefix non-inline URLs with this path.')


def main():
    args = parser.parse_args()
    sass_images.generate_sass_from_dir(args.dir, args.output,
                                       args.threshold, args.prefix)


if __name__ == '__main__':
    main()
