#!/bin/bash
source ./install_brilcalc.sh


awk '{print "./run_brilcalc_run.sh",$1}' $1 | bash > testlumi.txt
./colsum 1 testlumi.txt
