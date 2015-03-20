########################################################################
### this script:
### 1. specifies connectivity between LGN-PGN cells
### USE $ nrngui -python filename.py TO RUN
########################################################################
### import things
from neuron import h
import random
# h.load_file("RE_preserved.tem")
# cell=h.REcell()
# print "soma_re.v =", cell.soma_re(0.5).v
########################################################################
file = open("reticular.hoc").read()
file = file.replace('ncells=1', 'ncells=2')
f = open("reticular.hoc", 'w')
f.write(file)
f.close()
########################################################################
h.load_file("reticular.hoc")
#recell=h.REcell()
for sections in h.allsec():
	print sections.name()
print "------------------------------------------------------"
########################################################################
# making a dictionary contains secname() for proximal/distal...
d = {
   'a' : [1, 2, 3],
   'b' : [4, 5]
}

reticular = {
	'soma':['soma_re'], 
	'proximal':['dend_re1','dend_re3'], 
	'distal':['dend_re2','dend_re4']
}
print 'proximal =', reticular['proximal']
########################################################################
# create a list contains proximal dendrites of reticular cell
proximal = []
proximalname =[]
for prox in h.allsec():
	if 'REcell[0].soma_re' in prox.name():
		proximal.append(prox)
		proximalname.append(prox.name())
#	elif 'REcell[0].dend_re1[15]' in prox.name():
#		proximal.append(prox)

selectedprox = random.sample(proximal,  1)
print 's.sec: ', proximal
print 's.name: ', proximalname
print 'proximal dendrites:', selectedprox
print '------------------------------------------------------'

# create a list contains medial dendrites of reticular cell


# create a list contains distal dendrites of reticular cell
distal = []
distalname=[]
for dist in h.allsec():
	if 'REcell[1].dend_re3[13]' in dist.name():
		distal.append(dist)
		distalname.append(dist.name())
#	elif 'REcell[1].dend_re1' in dist.name():
#		distal.append(dist)

selecteddist = random.sample(distal, 1)  # Choose 2 elements
print 'r.sec: ',distal
print 'r.name: ',distalname
print 'distal dendrites: ', selecteddist

sender=proximal[0]
receiver=distal[0]
# making connections 
# NEURON equvalence: REcell[0].soma_re syn = new AMPA(0.5)
# no error! : nc=h.NetCon(cell.soma_re(0.5)._ref_v, None, sec=cell.soma_re)
syn = h.AMPA(0.5, sec=receiver)
nc=h.NetCon(sender(0.5)._ref_v, syn)
nc.weight[0]=0.2


########################################################################
vec = {}
for var in 'v_sender', 'v_receiver', 'i_syn', 't':
	vec[var] = h.Vector()

# record the membrane potentials and
# synaptic currents
vec['v_sender'].record(sender(0.5)._ref_v)
vec['v_receiver'].record(receiver(0.5)._ref_v)
vec['i_syn'].record(syn._ref_i)
vec['t'].record(h._ref_t)

# run the simulation
h.load_file("stdrun.hoc")
h.init()
h.tstop = 2300
h.run()

import matplotlib.pylab as plt                       
plt.subplot(2,1,1)
plt.xlabel('t (ms)')
plt.ylabel('v (mV)')
#plt.legend(['sender', 'receiver'])
#plt.plot(vec['t'], vec['v_sender'],
 #          vec['t'], vec['v_receiver'])
plt.plot(vec['t'], vec['v_sender'], label = 'sender')
plt.plot(vec['t'], vec['v_receiver'], 'r', label = 'receiver')
plt.legend(loc='upper left')
plt.subplot(2,1,2)
plt.plot(vec['t'], vec['i_syn'])
plt.ylim(-1, 2.0)
plt.show()
########################################################################