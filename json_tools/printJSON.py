#!/usr/bin/env python

import sys
import optparse
from LumiList import LumiList


if __name__ == '__main__':
    
    parser = optparse.OptionParser ("Usage: %prog alpha.json")
    parser.add_option ('--range', dest='range', action='store_true',
                       help='Print out run range only')
    parser.add_option ('--min', dest='minRun', action='store_true',
                       help='Print out minimum run number')
    parser.add_option ('--max', dest='maxRun', action='store_true',
                       help='Print out maximum run number')
    # required parameters
    (options, args) = parser.parse_args()
    if len (args) != 1:
        raise RuntimeError("Must provide exactly one input file")

    alphaList = LumiList (filename = args[0])  # Read in first  JSON file
    keys = alphaList.compactList.keys()
    minRun = min (keys)
    maxRun = max (keys)
    if options.range:
        print "runs %s - %s" % (minRun, maxRun)
        sys.exit()
    elif options.minRun:
        print "%s" % (minRun)
        sys.exit()
    elif options.maxRun:
        print "%s" % (maxRun)
        sys.exit()
    print alphaList
