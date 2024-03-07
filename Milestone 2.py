import math
import numpy as np
import matplotlib.pyplot as plt
import sounddevice as sd
from scipy.fftpack import fft

t = np.linspace(0 , 3 , 12 * 1024)
octave3= [130.81,146.83,164.81,174.61]
octave4= [261.63,293.66,329.63,349.23]

N= 3*1024 ##Num of samples
f= np.linspace(0,512,int(N/2))
f1= octave3[3]
f2= octave4[0]

StartTime= [0,     1,       1.3,     2.3]
TimePeriod=[0.4,   0.2 ,      1,      0.2]
n=3 ## Num of pairs of notes
i=0
x=0
while(n>i):
    o3= octave3[i]
    o4= octave4[i]
    Ti= StartTime[i]
    T2= TimePeriod[i]
    note1= np.sin(2*np.pi*o3*t)
    note2= np.sin(2*np.pi*o4*t)
    x= x+ ((note1+note2)*((t>=Ti) & (t<=Ti+T2)))
    i=i+1
  

## Picking random noise frequencies, getting their total frequency
f1_n= np.random.randint(0,512,1)
f2_n= np.random.randint(0,512,1)
noise = np.sin(2*f1_n*np.pi*t) + np.sin(2*f2_n*np.pi*t)


##x(t) **with** noise added on top in time domain
x_n = x+noise 

##x(t) **without** the noise in freq domain
xt_f = fft(x)
xt_f= 2/N * np.abs(xt_f[0:int(N/2)])  

##x(t) **with** the noise in freq domain
xn_f = fft(x_n)
xn_f= 2/N * np.abs(xn_f[0:int(N/2)])   


## getting the pair of noise frequencies from xn_f (x(t) **with** noise in freq domain))
maxVal = math.ceil(np.max(xt_f))

fi=0
freq=[]
for fi in range(0,np.size(xn_f),1):
    if(xn_f[fi]>maxVal):
        freq=np.append(freq,math.floor(f[fi]))
    fi= fi+1


## Filtered song in time domain
x_filtered= x_n-( (np.sin(2*freq[0]*np.pi*t)) + (np.sin(2*freq[1]*np.pi*t)) )


##Filtered song in freq domain
xn_filtered= fft(x_filtered)
xn_filtered= 2/N * np.abs(xn_filtered[0:int(N/2)])  


sd.play(x,3*1024) 
##sd.play(x_filtered,3*1024)


plt.subplot(3,3,1)
plt.plot(t,x)
plt.xlabel("Song(t) w/o noise")
plt.subplot(3,3,2)
plt.plot(f,xt_f)
plt.xlabel("Song(n) w/o Noise")
plt.subplot(3,3,3)
plt.plot(t,x_n)
plt.xlabel("Song(t) w/ noise")
plt.subplot(3,3,4)
plt.plot(f,xn_f)
plt.xlabel("Song(n) w/ noise")
plt.subplot(3,3,5)
plt.plot(t,x_filtered)
plt.xlabel("Filtered Song(t)")
plt.subplot(3,3,6)
plt.plot(f,xn_filtered)
plt.xlabel("Filtered Song(n)")

"""
plt.figure()
plt.plot(t,x)
plt.xlabel("Song in time domain without noise")
plt.figure()
plt.plot(f,xt_f)
plt.xlabel("Song in freq domain without noise")
plt.figure()
plt.plot(t,x_n)
plt.xlabel("Song in time domain with noise")
plt.figure()
plt.plot(f,xn_f)
plt.xlabel("Song in freq domain with noise")
plt.figure()
plt.plot(t,x_filtered)
plt.xlabel("Filtered Song in time domain")
plt.figure()
plt.plot(f,xn_filtered)
plt.xlabel("Filtered Song in freq domain")
"""





