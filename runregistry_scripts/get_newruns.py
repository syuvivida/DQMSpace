#!/usr/bin/env python 
import runregistry 
import argparse 
import sys 


def runs_list(filter_in):  
  runs = runregistry.get_runs(filter = filter_in) 
  return runs 


if __name__ == '__main__': 
     
    parser = argparse.ArgumentParser( 
            description='Give list of the latest collision runs')
    parser.add_argument("-o", "--outfile", 
        dest="outfile", type=str, default="newRuns", help="Output file name") 
    parser.add_argument("-min", "--min_run", dest="min_run", type=int, default=355100, help="minimum run for json") 
    parser.add_argument("-max", "--max_run", dest="max_run",type=int, default=999999, help="maximum run for json")  
    options = parser.parse_args() 
    print(sys.argv)
 
   # generate filter  
    filter_arg = { 'run_number': { 'and':[ {'>=': options.min_run}, {'<=': options.max_run}] },  
                   'class': { 'like': 'Collisions22%'}, 
                   'oms_attributes.b_field': {">=": 3.7} 
	          }
 
    out_runs = runs_list(filter_arg) 
    sys.stdout = open(options.outfile, "w")
    for run in out_runs:  
      print(run["run_number"])

    sys.stdout.close()
