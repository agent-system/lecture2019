#!/bin/bash
roscd aizuspider_description
./move.py --trans -0.9 --name AizuSpiderAA
./move.py --rot -0.6 --name AizuSpiderAA
./move.py --trans -3.5 --name AizuSpiderAA
./move.py --rot -0.7 --name AizuSpiderAA
cd /userdir
