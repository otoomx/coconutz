## Coconut Delivery - Solution by Mike O'Toole

This program is a solution to coconut delivery problem expressed at https://github.com/AdamFinch1/coconut_delivery

Overview
--------
The program is designed to read in a data that represents a set of jetstream paths and calculates the most efficient route, based on each jetstreams weight

#### Assumptions
* The Swallow will start at mile marker 0 when he starts his coconut deliver journey
* The destination is always the greatest mile marker in the data file
* Not all jetstream paths are connected and the program will need to create routes between jetstreams that are not connected


Running the program
-------------------

The program was designed to run with Python 2.7.x

To run the program execute it from the command line as follows
```
python main.py -i input_file_name

```

#### Example Results
```
Total Energy consumed on most efficient route: 352
Most Efficient route: 
[(0, 5), (6, 11), (14, 17), (19, 24)]
```