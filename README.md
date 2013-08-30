mp3
===

Fixes cyrillic mp3 tags.



## Why?

Why I wrote this? Why didn't I use something already out there? Here is reason: 
1. Couple scripts I found were incredibly hard to read and undestand logic. 
2. I don't understand why user need to answer questions during script execution. 
3. I don't like Java. There is java version of converter, which works. 


## Requirements:
* Python 2.7 (should work on 2.6, didn't test)
* eyed3


## Installation instructions

### Install eyeD3

    pip install eyed3 

or follow instructions - http://eyed3.nicfit.net/installation.html

Then run `./mp3_fixer.py --help` to get help. 


## Help

    positional arguments:
      dir                  Folder with mp3 files to fix.

    optional arguments:
     -h, --help           show this help message and exit
     --debug              Show debug output
     --dry-run            Don't write changes to disk.
     --encoding ENCODING  Encoding of the tags in your mp3 files.
     -v, --version        show program's version number and exit


Possible encodings are cp1251, koi8-r
