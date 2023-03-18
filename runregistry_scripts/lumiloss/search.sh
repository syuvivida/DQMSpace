#!/bin/bash


runNumber=$1
for iteration in {B,C,D,E,F,G}
do
#  echo $iteration
  grep -a $runNumber Era/era${iteration}_runs.txt
  if [ $? -eq 0 ]; then 
      echo -e "\n"
      echo "$runNumber is in Era $iteration"
      echo -e "\n"
  fi
done


