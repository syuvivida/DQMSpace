#!/bin/bash
#Note, the end date needs to add 1 day
# 08/18/22 - 08/24/22
brilcalc lumi -b "STABLE BEAMS" --byls --beamenergy 6800 --amodetag PROTPHYS --begin $1' 00:00:00' --end $2' 00:00:00' -u /fb
