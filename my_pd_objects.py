# Pyext library only available within PD/pyext environment.
try:
    import pyext
except:
    print "ERROR: This script must be loaded by the PD/Max pyext external"

# Set my working directory to the one where this script is located
import os
#import chords1 as ch
import MarkChords as ch
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)
print(dname)

#import modules (yours or python's)
#from generator import Generator 

# This class represents a pd object
# [pyext my_pd_objects.simple_object]
class simple_object(pyext._class): 
    # There is one inlet (the leftmost) and one outlet (the rightmost) by default.
    # Add more here:
    _inlets=3  # 3 inlets total. 
    # The leftmost inlet is used to receive a "reload" message to refresh the object
    # when you chnage the code
    
    _outlets=4 # 3 outlets total

    i=0
    N=0
    cond=0


    def gen_1(self, *args):
        # Args is a tuple with the atoms of the load message from PD
        self.N=args[0]
        self.seq=ch.chord_prog(self.N, self.cond)
        self.i=0
        print ('\n Secuencia:')
        print(self.seq)


    # This method will be triggered when a "search" message is received on the second inlet
    def newChord_3(self, *args): 

        chord=self.seq[self.i]
        print(chord)
        
        for c in range(len(chord)):
           self._outlet(c+1, chord[c])
           if (len(chord)==3):
              self._outlet(4, 0)
        
        self.i=self.i+1
        if self.i == (self.N):
            self.i=0

    def cond_2(self, *args): 
        self.cond=args[0]
        print(self.cond)
##########################################################################


