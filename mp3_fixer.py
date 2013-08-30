#!/usr/bin/env python
from __future__ import print_function

import os
import argparse
import fnmatch
import logging

import eyed3
import eyed3.mp3

VERSION = "0.1"
ENCODING = ['cp1251', 'koi8-r']

# TODO: add tests
# TODO: delete v1 tags, and save v2 tas only. 
# TODO: generate some statistics (???)

# Why I wrote this? Why didn't I use something already out there? Here is reason: 
# 1. Couple scripts I found were incredibly hard to read and undestand logic. 
# 2. I don't understand why user need to answer questions during script execution. 
# 3. I don't like Java. There is java version of converter, which works. 


# Requirements: Python 2.7 (should work on 2.6, didn't test), eyed3
# Installation instructions: 
# pip install eyed3 or follow instructions - http://eyed3.nicfit.net/installation.html
# and then run me with --help. 

# Possible encodings are cp1251, koi8-r

# TOFix: For some reason eyed3 takes over logging. 
# formatter = logging.Formatter('%(levelname)s: %(message)s')
# console_handler = logging.StreamHandler()
# console_handler.setFormatter(formatter)
log = logging.getLogger('mp3')
# log.addHandler(console_handler)


def is_ascii(s):
    """Checks if text is in ascii. 
    Thanks to this thread on StackOverflow: http://stackoverflow.com/a/196392/881330
    """
    return all(ord(c) < 256 for c in s)


def fix_encoding(s, encoding):
    """Fixes encoding. It does some magic. :-) 
    Thanks going to this StackOverflow thred: http://stackoverflow.com/a/14168052/881330
    """
    if s:
        if is_ascii(s):
            fixed = s.encode('latin-1').decode(encoding)
        else:
            fixed = s
        if fixed != s:
            log.info(" Converting '%s' into '%s'.", s, fixed)
        return fixed


def process_folder(dir_name, encoding, dry_run):
    """Searches for mp3 files and converts tags. 
    """
    files = []
    for r, d, fl in os.walk(dir_name):
        for f in fnmatch.filter(fl, '*.mp3'):
            files.append(os.path.join(r, f))
    for file in files:
        if eyed3.mp3.isMp3File(file):
            log.info("Processing file '%s'..." % (file))
            f = eyed3.load(file)
            if f.tag:
                log.info(" Tag version: %s", eyed3.id3.versionToString(f.tag.version))
                # TODO: go and fix *ALL* tags, not just three.
                f.tag.album = fix_encoding(f.tag.album, encoding)
                f.tag.artist = fix_encoding(f.tag.artist, encoding)
                f.tag.title = fix_encoding(f.tag.title, encoding)
                if not dry_run:
                    f.tag.save(encoding='utf-8', version=eyed3.id3.ID3_V2_4)
                    log.info(" Saving file.")
                log.info("Completed processing file '%s'.", file)

            else:
                log.warn(' No tags found.')
        else:
            log.warn("File '%s' is not mp3 file.", file)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Converts wrongly encoded Cyrilic mp3 tags into Unicode.')
    parser.add_argument('dir', help='Folder with mp3 files to fix.')
    parser.add_argument('--debug', action='store_true', help='Show debug output')
    parser.add_argument('--dry-run', action='store_true', default=False, help='Don\'t write changes to disk.')
    parser.add_argument('--encoding', default='cp1251', choices=ENCODING, help='Encoding of the tags in your mp3 files.')
    parser.add_argument('-v', '--version', action='version', version='%(prog)s {}'.format(VERSION))

    args = parser.parse_args()

    if args.debug:
        log.setLevel(logging.DEBUG)
    else:
        log.setLevel(logging.INFO)

    log.debug('Dir: %s', args.dir)
    log.debug('dry-run: %s', args.dry_run)
    log.debug('encoding: %s', args.encoding)

    if os.path.exists(args.dir):
        log.info("Processing folder '%s'", args.dir)
        process_folder(args.dir, args.encoding, args.dry_run)
    else:
        log.info("Error: folder '%s' not found.", args.dir)
