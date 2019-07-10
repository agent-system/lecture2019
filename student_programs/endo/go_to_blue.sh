#!/bin/bash
roscd aizuspider_description
python solve_ik.py
./move.py --trans -1.5 --name AizuSpiderAA
./move.py --rot -0.9 --name AizuSpiderAA
./move.py --rot -0.9 --name AizuSpiderAA
./move.py --trans 1.2 --name AizuSpiderAA
./move.py --rot -0.45 --name AizuSpiderAA
./move.py --trans 1.2 --name AizuSpiderAA
cd /userdir
