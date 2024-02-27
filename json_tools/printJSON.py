#!/usr/bin/env python3

import sys
from argparse import ArgumentParser
from LumiList import LumiList

if __name__ == '__main__':
    
    parser = ArgumentParser()
    parser.add_argument('--range', dest='range', default=True, action='store_true',
                         help='Print out run range only')
    parser.add_argument("alpha_json", metavar="alpha.json", type=str)
    parser.add_argument('--min', dest='minRun', action='store_true',
		       help='Print out minimum run number')
    parser.add_argument('--max', dest='maxRun', action='store_true',
		       help='Print out maximum run number')
    options = parser.parse_args()

    alphaList = LumiList (filename = options.alpha_json) # Read in first JSON file
    if options.range:
        keys = list(alphaList.compactList.keys())
        minRun = min (keys)
        maxRun = max (keys)
        print(("runs %s - %s" % (minRun, maxRun)))
        print(("%s" % (minRun)))
        print(("%s" % (maxRun)))
        sys.exit()
    elif options.minRun:
        print(("%s" % (minRun)))
        sys.exit()
    elif options.maxRun:
        print(("%s" % (maxRun)))
        sys.exit()

    print(alphaList)
