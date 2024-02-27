#!/usr/bin/env python3

import sys
import os.path
import optparse
import json

if __name__ == '__main__':
    
    parser = optparse.OptionParser ("Usage: %prog alpha.json")
    # required parameters
    (options, args) = parser.parse_args()
    if len (args) != 1:
        raise RuntimeError("Must provide exactly one input file")

    filename = args[0]  # Read in first  JSON file
    # check if a file exists first
    if not os.path.exists(filename):
        print(("%s does not exist" % (filename)))
        sys.exit(1)

    if not os.path.isfile(filename):
        print(("%s is not a file" % (filename)))
        sys.exit(1)
    
    with open(filename, 'rb') as file:
        json_file = open(filename)
        json_data = json.load(json_file)
        if len(json_data) == 0:
            print(("%s is an empty JSON file" % (filename)))
            sys.exit(1)

 
    sys.exit(0)

