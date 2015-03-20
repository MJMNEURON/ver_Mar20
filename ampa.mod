NEURON {
	POINT_PROCESS AMPA
}

PARAMETER {
  Cdur	= 0.3	(ms)		: transmitter duration (rising phase)
  Alpha	= 0.47	(/ms mM)	: forward (binding) rate
  Beta	= 0.18	(/ms)		: backward (unbinding) rate
  Erev	= 0	(mV)		: reversal potential
}


INDEPENDENT {t FROM 0 TO 1 WITH 1 (ms)}

NEURON {
  RANGE g, Erev
  NONSPECIFIC_CURRENT i
  GLOBAL Cdur, Alpha, Beta, Rinf, Rtau
}

UNITS {
  (nA) = (nanoamp)
  (mV) = (millivolt)
  (umho) = (micromho)
  (mM) = (milli/liter)
}

ASSIGNED {
  v		(mV)		: postsynaptic voltage
  i 		(nA)		: current = g*(v - Erev)
  g 		(umho)		: conductance
  Rinf				: steady state channels open
  Rtau		(ms)		: time constant of channel binding
  synon
}

STATE {Ron Roff}

INITIAL {
  Rinf = Alpha / (Alpha + Beta)
  Rtau = 1 / (Alpha + Beta)
  synon = 0
}

BREAKPOINT {
  SOLVE release METHOD cnexp
  g = (Ron + Roff)*1(umho)
  i = g*(v - Erev)
}

DERIVATIVE release {
  Ron' = (synon*Rinf - Ron)/Rtau
  Roff' = -Beta*Roff
}

: following supports both saturation from single input and
: summation from multiple inputs
: if spike occurs during CDur then new off time is t + CDur
: ie. transmitter concatenates but does not summate
: Note: automatic initialization of all reference args to 0 except first

NET_RECEIVE(weight, on, nspike, r0, t0 (ms)) {
  : flag is an implicit argument of NET_RECEIVE and  normally 0
  if (t>0) { : bug fix so that init doesn't send a false event
    if (flag == 0) { : a spike, so turn on if not already in a Cdur pulse
      nspike = nspike + 1
      if (!on) {
        r0 = r0*Exp1(-Beta*(t - t0))
        t0 = t
        on = 1
        synon = synon + weight
        Ron = Ron + r0
        Roff = Roff - r0
      }
      : come again in Cdur with flag = current value of nspike
      net_send(Cdur, nspike)
    }
    if (flag == nspike) { : if this associated with last spike then turn off
      r0 = weight*Rinf + (r0 - weight*Rinf)*Exp1(-(t - t0)/Rtau)
      t0 = t
      synon = synon - weight
      Ron = Ron - r0
      Roff = Roff + r0
      on = 0
    }
  }
}

FUNCTION Exp1(x) {   
  if (x < -100) {
    Exp1  = 0
  } else if (x > 100) {
    Exp1 = exp(100)
  } else{
    Exp1 = exp(x)
  }
}