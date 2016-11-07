#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt

fig, ax = plt.subplots()

cut_lengths = [0, 2, 5, 7.5, 10, 100]
PD = [0, 0.76, 0.888, 0.897, 0.919, 0.962]

x = np.array(cut_lengths)
y = np.array(PD)

plt.plot(x, y, 'b-o')
#plt.minorticks_on()
#plt.grid(b=True, which='minor')
#plt.grid(b=True, which='minor')
plt.grid(True)

#ax.set_xticklabels(np.linspace(0,100,21))
plt.xticks([0,5,10,20,30,40,50,60,70,80,90,100])


plt.xlabel('Sequence Length (kbp)',fontsize=18)
plt.ylabel('Predictive Discrimination',fontsize=18)

plt.savefig('ppv_vs_sl.png')
plt.show()
