#!/usr/bin/env python
# main.py
# Coconut Delivery System 
# solution to https://github.com/AdamFinch1/coconut_delivery
import re
import sys
import getopt

__author__      = "Mike O'Toole otoolem@gmail.com"

def main():


    try:

        if len(sys.argv)==1:
            raise  getopt.GetoptError("No Options supplied")
            print_usage()
        opts, args = getopt.getopt(sys.argv[1:], "hi:")

        for o, a in opts:
         
            if o == "-v":
                verbose = True
            elif o in ("-h"):
                print_usage()
                sys.exit()
            elif o in ("-i"):
                input = a
                process_graph(input)
            else:
                raise  getopt.GetoptError("Invalid Option: {}".format(o))


        
    
    except getopt.GetoptError as err:
        # print help information and exit:
        print str(err) # will print something like "option -a not recognized"
        print_usage()
        sys.exit(2)

def process_graph(input_file):
    print input_file

def print_usage():

    print "Usage: python main.py [options ...]"
    print "-h \t display usage information"
    print "-i <filename>\t filename to parse"
    print "Example: python main.py -h sample.txt"

if __name__ == '__main__':
   main()