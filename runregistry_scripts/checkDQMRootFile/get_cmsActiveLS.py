#!/usr/bin/env python 
import runregistry 
import argparse 
import sys 
if __name__ == '__main__': 
     
    parser = argparse.ArgumentParser( 
            description='Give OMS information')
    parser.add_argument("-r", "--runNumber", dest="runNumber", type=int, default=367355, help="run number") 
    options = parser.parse_args() 

    run = runregistry.get_run(run_number=options.runNumber)
#    print(run)
    LS = run['oms_attributes']['last_lumisection_number']
 
    print(LS)
