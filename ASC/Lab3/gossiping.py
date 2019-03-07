"""
Implementati o propagare ciclica de tip gossiping folosind bariere. 
  * Se considera N noduri (obiecte de tip Thread), cu indecsi 0...N-1.
  * Fiecare nod tine o valoare generata random.
  * Calculati valoarea minima folosind urmatorul procedeu:
     * nodurile ruleaza in cicluri
     * intr-un ciclu, fiecare nod comunica cu un subset de alte noduri pentru a
       obtine valoarea acestora si a o compara cu a sa
       * ca subset considerati random 3 noduri din lista de noduri primita in
        constructor si obtineti valoarea acestora (metoda get_value)
     * dupa terminarea unui ciclu, fiecare nod va avea ca valoare minimul
       obtinut in ciclul anterior
     * la finalul iteratiei toate nodurile vor contine valoarea minima
  * Folositi una din barierele reentrante din modulul barrier.
  * Pentru a simplifica implementarea, e folosit un numar fix de cicluri,
    negarantand astfel convergenta tutoror nodurilor la acelasi minim.
"""

import sys
import random
from threading import Thread
from barrier import SimpleBarrier, ReusableBarrierCond, ReusableBarrierSem

random.seed(0) # genereaza tot timpul aceeasi secventa pseudo-random
global min_list

class Node(Thread):
    #TODO_ Node trebuie sa fie Thread

    def __init__(self, node_id, all_nodes, num_iter, reuse_barrier):
        #TODO_ nodurile trebuie sa foloseasca un obiect bariera

        Thread.__init__(self)
        self.node_id = node_id
        self.all_nodes = all_nodes
        self.num_iter = num_iter
        self.value = random.randint(1, 1000)
        self.t_barrier = reuse_barrier

    def set_nodes(self, nodes):
        self.all_nodes = nodes

    def run(self):
        for i in xrange(num_iter):
            #get neighbours
            neighs = [random.randint(0, len(self.all_nodes) - 1),\
                      random.randint(0, len(self.all_nodes) - 1),\
                      random.randint(0, len(self.all_nodes) - 1)]
            #get values
            neigh_vals = list(map(lambda ind: self.all_nodes[ind].get_value(), neighs))
            #find min
            my_min = min([self.value] + neigh_vals)

            #wait all to find their min
            self.t_barrier.wait()
            #set value
            self.value = my_min
            min_list[self.node_id] = my_min
            #print self.name, 'have min', my_min
            #wait all to set the value
            self.t_barrier.wait()
         
    def get_value(self):
        return self.value

if __name__ == "__main__":
    if len(sys.argv) == 2:
        num_threads = int(sys.argv[1])
    else:
        print "Usage: python " + sys.argv[0] + " num_nodes"
        sys.exit(0)

    num_iter = 3  # numar iteratii/cicluri algoritm

    #TODO_ Create nodes and start them
    ts_barrier = ReusableBarrierCond(num_threads)
    threads = [Node(i, num_threads, num_iter, ts_barrier) for i in xrange(num_threads)]
    min_list = [0 for i in xrange(num_threads)]
    for t in threads:
        t.set_nodes(threads)

    for t in threads:
        t.start()

    #TODO_ Wait for nodes to finish
    for t in threads:
        t.join()
    print min_list
