Instructions on running blockmaze.py
A description of blockmaze.py can be found in project1.pdf


In the command line, type:


python3 blockmaze.py [file] [heuristic]


where file is the location of a valid maze file and heuristic is either “manhattan” or “trivial”
Valid maze files can be found in the examples folder- labeled “maze_.txt”


Example calls of the program:
python3 blockmaze.py examples/maze5.txt manhattan
python3 blockmaze.py examples/maze2.txt trivial


Invalid calls: 
python3 blockmaze.py
python3 blockmaze.py examples/maze5.txt
python3 blockmaze.py manhattan
etc…