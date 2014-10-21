#!/usr/bin/env python
# main.py
# Coconut Delivery System 
# solution to https://github.com/AdamFinch1/coconut_delivery

import sys
import getopt
import heapq
import pprint


__author__      = "Mike O'Toole otoolem@gmail.com"

#   Graph class represents the JetStream as a weighted directed graph
#   
class Graph(object):

    def __init__(self,default_energy):
  
        self.vertices = {}
        self.default_energy = default_energy
        self.last_node = 0

    # add a vertex to the graph
    # params vertex (mile marker)
    def add_vertex(self,v):
        self.vertices[v] = Vertex(v)
        if v > self.last_node  :
            self.last_node=v
            

    # add a weighted edge
    # params start point, end point, weight (energy), 
    # is_jetstream (is the edge on the jetstream, default is False)
    def add_edge(self,start_point,end_point,weight,is_jetstream=False):
        #initilize the vertices if they are already there
        if start_point not in self.vertices:
            self.add_vertex(start_point)

        if end_point not in self.vertices:
            self.add_vertex(end_point)


        #add the neighbors

        edge = Edge(start_point,end_point,weight,is_jetstream)
        self.vertices[start_point].add_neighbor(edge)


    # Compute shortest path from start node all the way to end node
    # params start_point, end_point
    # uses dijkistras algorythm 
    # http://en.wikipedia.org/wiki/Dijkstra's_algorithm#Using_a_priority_queue
    # inspired by: http://code.activestate.com/recipes/119466-dijkstras-algorithm-for-shortest-paths/
    def compute_efficient_paths(self, start_point, end_point):

        ##before we can perform the search we need to fill in the gaps
        ##between the jetstream nodes where there is no connection

        #fill in gaps between jetstream nodes by traveling 
        #without jetstream
        self.connect_jetstreams()

        #set up a queue
        queue = []


        ##itilize vertices distance from the start
        for vertex in self.vertices:
            if vertex == start_point:
                # first node should be zero distance
                self.vertices[vertex].distance = 0
            else: 
                # set the rest to an unreachable distance
                self.vertices[vertex].distance = sys.maxsize

            #push em on the queue
            heapq.heappush(queue, [self.vertices[vertex].distance, vertex])

        while queue:
            lowest_vertex = heapq.heappop(queue)[1]
            self.vertices[lowest_vertex].visited = True

            for neighbor in self.vertices[lowest_vertex].neighbors:
                if(self.vertices[neighbor].visited <> True):
                    new_distance = self.vertices[lowest_vertex].distance + self.vertices[lowest_vertex].neighbors[neighbor].weight

                    if new_distance < self.vertices[neighbor].distance:
                        self.vertices[neighbor].distance = new_distance
                        self.vertices[neighbor].previous = lowest_vertex
                        #update queue priority  
                        for v in queue:
                            if v[1] == neighbor:
                                v[0] = new_distance
                                break
                        heapq.heapify(queue)

    # Return the shortest path from the start to an endpoint
    # return: path array of tuples, total amount of energy
    def get_best_path(self, end_point):
        
        path = []
        current_node = end_point

        #connec the dots between nodes to create an array of best paths
        while(self.vertices[current_node].previous != None):
            previous_node = self.vertices[current_node].previous
            #get edge so we can inspect information
            edge =  self.vertices[previous_node].neighbors[current_node]

            #only include jetstream elements in the path
            if edge.is_jetstream_edge:
                path.insert(0, (previous_node , current_node))

            current_node = previous_node

        #return the path along with the total energy
        total_distance = self.vertices[end_point].distance
        return path, total_distance


    # Fills in the gaps between jetstream paths
    # which allows the bird to travel on edges that are not on the jetstream
    # in order to connect to jetstream edges
    def connect_jetstreams(self):
        nodes = self.vertices.keys()
  
        node_length = len(nodes)

        if(node_length==0):
            return

        #sort the node keys
        nodes.sort()

        ##if the first node is not 0 connect zero to the first node

        if(nodes[0]!=0):
             self.add_edge(0,nodes[0], nodes[0]*self.default_energy)

        for i in range(node_length-1):
        
            current_node = nodes[i]
            next_node = nodes[i+1]

            if(next_node not in self.vertices[current_node].neighbors):
                weight = (next_node - current_node) * self.default_energy
                self.add_edge(current_node, next_node, weight)


    def __str__(self):
        return str(self.vertices)

#class represents the node or vertex on the graph
class Vertex(object):

    def __init__(self,id):
        self.id = id
        self.neighbors = {}
        self.distance = sys.maxsize #default distance, unreachable
        self.previous = None #default undefined
        self.visited = False

    def add_neighbor(self, edge):
        self.neighbors[edge.end_node] = edge

    def get_neighbors(self):
        return self.neighbors

    def __str__(self):
        return str(self.id)
#class represents the connection between two nodes on the graph
class Edge(object):

    def __init__(self, start_node,end_node, weight, is_jetstream_edge):
        self.start_node = start_node
        self.end_node = end_node
        self.weight = weight
        self.is_jetstream_edge = is_jetstream_edge

    def __str__(self):
        return "edge:{} {} weight:{} on the jetstream: {}".format(self.start_node,self.end_node,self.weight, self.is_jetstream_edge)

# main program method
def main():

    try:

        if len(sys.argv)==1:
            raise  getopt.GetoptError("No Options supplied")
            print_usage()

        opts, args = getopt.getopt(sys.argv[1:], "hi:")

        if( len(opts)==0    ):
            raise  getopt.GetoptError("No Options supplied")
            print_usage()
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

# processes the input file and loads into a graph
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
            graph.add_edge(start_point,end_point,energy, True)
   
        ##get the shortest path
        graph.compute_efficient_paths(0,graph.last_node)

        #retrieve the path and distance to the last node
        jetstream_path, energy_used = graph.get_best_path(graph.last_node)
        
        print "Total Energy consumed on most efficient route: {}".format(energy_used)

        print "Most Efficient route: "
        
        #pretty print the path info
        pprint.pprint(jetstream_path)
        
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