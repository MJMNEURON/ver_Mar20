########################################################################
###### import things
from neuron import h
import random
from random import randint
import matplotlib.pylab as plt
# h.load_file("RE_preserved.tem")
# cell=h.REcell()
# print "soma_re.v =", cell.soma_re(0.5).v
########################################################################
file = open("reticular.hoc").read()
file = file.replace('ncells=2', 'ncells=3')
f = open("reticular.hoc", 'w')
f.write(file)
f.close()
########################################################################
h.load_file("reticular.hoc")
########################################################################
###### making a dictionary contains secname() for proximal/distal...
record = {
	'soma_re0': ['[0].soma_re'],
	'dend_receiver': ['REcell[1].dend_re4']
}
reticular = {
	'soma':['[0].soma_re'], 
	'proximal':['REcell[0].dend_re1[2]', 'REcell[0].dend_re2[2]', '[0].soma_re'], 
	'distal':['[1].dend_re4', '[2].dend_re4']
}
#print 'proximal =', reticular['proximal']
########################################################################
###### create a list contains proximal dendrites of reticular cell
proximal = []
proximalname =[]
for prox in h.allsec(): # print prox.name() # gives out REcell[0].soma_re......
	if any(s in prox.name() for s in reticular['proximal']):
		proximal.append(prox)
		proximalname.append(prox.name())
print "PROXI_NAME", proximalname
selprox = random.sample(proximal,  3)
selproxname = random.sample(proximalname,  3)

#print 's.sec: ', proximal, '\n'
print 's.name: ', proximalname, '\n'
print 'proximal dendrites:', selprox, '\n', selproxname
print '------------------------------------------------------'
###### create a list contains distal dendrites of reticular cell
distal = []
distalname=[]
for dist in h.allsec():
	if any(s in dist.name() for s in reticular['distal']):
		distal.append(dist)
		distalname.append(dist.name())

seldist = random.sample(distal, 3)  # Choose n elements
seldistname = random.sample(distalname,  3)
#print 'r.sec: ',distal
print 'r.name: ',distalname, '\n'
print 'distal dendrites: ', seldist, '\n', seldistname
print '------------------------------------------------------'
#print seldistname[1]
########################################################################
###### randomly selecting n secs from the list of secs
send = []
receive = []
syn = []
nc = []
vec = {}
for counter in range (0, 3): # (0, how many secs to take)
	nprox = randint(0, len(selprox)-1)	
	send.append(selprox[nprox])
	ndist = randint(0, len(seldist)-1)
	receive.append(seldist[ndist])
	syni = h.AMPA(0.5, sec = receive[counter])
	syn.append(syni)
	nci=h.NetCon(send[counter](0.5)._ref_v, syni, sec=send[counter])
	nci.weight[0] = 0.2
	nc.append(nci)

	#print selprox[nprox]
	print "sender[counter] = ", send[counter].name()
	print "receiver[counter] = ", receive[counter].name()

	selprox.remove(selprox[nprox])
	seldist.remove(seldist[ndist])
########################################################################
soma=[]
for recs in h.allsec():
	if any(s in recs.name() for s in record['soma_re0']):
		soma.append(recs)
print soma[0].name()

dend=[]
for recd in h.allsec():
	if any(s in recd.name() for s in record['dend_receiver']):
		dend.append(recd)
print dend[0].name()

for var in 'v_sender', 'v_receiver', 'i_syn', 't':
	vec[var] = h.Vector()


vec['v_sender'].record(soma[0](0.5)._ref_v)
vec['v_receiver'].record(dend[0](0.5)._ref_v)
vec['i_syn'].record(syn[0]._ref_i)
vec['t'].record(h._ref_t)

h.load_file("stdrun.hoc")
h.init()
h.tstop = 2400
h.run()

plt.xlabel('t (ms)')
plt.ylabel('v (mV)')                       
plt.subplot(2,1,1)
plt.plot(vec['t'], vec['v_sender'], label=soma[0].name() )
plt.plot(vec['t'], vec['v_receiver'], 'r', label = dend[0].name())
plt.legend(loc='upper left')
plt.subplot(2,1, 2)
plt.plot(vec['t'], vec['i_syn'])
plt.ylim(-5, 2.0)	
plt.show()
########################################################################
