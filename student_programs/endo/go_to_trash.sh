#!/bin/bash
roscd aizuspider_description
python solve_ik.py
./move.py --trans -0.1 --name AizuSpiderAA
./move.py --rot 0.6 --name AizuSpiderAA
./move.py --trans 2 --name AizuSpiderAA
./move.py --rot -0.6 --name AizuSpiderAA
./move.py --trans 3.6 --name AizuSpiderAA
./move.py --rot 0.6 --name AizuSpiderAA
./move.py --trans 1.05 --name AizuSpiderAA
cd /userdir
