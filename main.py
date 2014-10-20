#!/usr/bin/env python
# main.py
# Coconut Delivery System 
# solution to https://github.com/AdamFinch1/coconut_delivery
import re
import sys
import getopt

__author__      = "Mike O'Toole otoolem@gmail.com"

class Graph(object):

    def __init__(self,default_energy):
  
        self.vertices = {}
        self.default_energy = default_energy
        self.last_node = 0

    def add_vertex(self,v):
        self.vertices[v] = Vertex(v)
        if v > self.last_node  :
            self.last_node=v
            


    def add_edge(self,start_point,end_point,weight,is_jetstream=False):
        #initilize the vertices if they are already there
        if start_point not in self.vertices:
            self.add_vertex(start_point)

        if end_point not in self.vertices:
            self.add_vertex(end_point)


        #add the neighbors
        self.vertices[start_point].add_neighbor(Edge(start_point,end_point,weight,is_jetstream))


    def get_shortest_path(self, start_point, end_point):
        print "getting shortest path"


#class represents the node or vertex on the graph
class Vertex(object):

    def __init__(self,id):
        self.id = id
        self.neighbors = {}

    def add_neighbor(self, edge):
        self.neighbors[edge.end_node] = edge

#class represents the connection between two nodes on the graph
class Edge(object):

    def __init__(self, start_node,end_node, weight, is_jetstream_edge):
        self.start_node = start_node
        self.end_node = end_node
        self.weight = weight
        self.is_jetstream_edge = is_jetstream_edge

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

    try:
        input_file = open(input_file)

        #file format is going to be like this:
        #50         //first line is the default energy consumption
        #0 5 10     //each addtional is a space seperated set of 
        #1 3 50     //three numbers (start mile, end mile, energy)
        #3 7 12     //this represents a jetstream path
        #6 11 20

        #first read the first line to get the default energy consumption
        default_energy = int(input_file.readline())

        #create a graph object
        graph = Graph(default_energy)
        
        #then loop through the rest of the lines to get the rest of the elements to build the graph
        for jetstream_line in input_file.readlines():
            edge_data =  jetstream_line.split()
            
            #cast the data elements to int
            start_point = int(edge_data[0])
            end_point = int(edge_data[1])
            energy = int(edge_data[2])
            graph.add_edge(start_point,end_point,energy)
   

        
       
        print graph.last_node

        
    except IOError as err:
        print str(err)
        exit(2)


def print_usage():

    print "Usage: python main.py [options ...]"
    print "-h \t display usage information"
    print "-i <filename>\t filename to parse"
    print "Example: python main.py -h sample.txt"

if __name__ == '__main__':
   main()