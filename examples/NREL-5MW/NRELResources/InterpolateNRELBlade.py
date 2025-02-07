import math
import argparse
import csv
#import f90nml
#import matplotlib
import numpy as np
from scipy import interpolate
#from pylab import *
#import matplotlib.pyplot as plt

parser = argparse.ArgumentParser(description="Script to extract Boundary Layer Flow statistics from *.dat files")
parser.add_argument("-v","--verbose",action="store_true",help="Print location")
parser.add_argument("-p","--plot",action="store_true",help="Plots the wake profiles")
parser.add_argument("-w","--write",action="store_true",help="Write results in a .csv file")
parser.add_argument("NumElem", type=int, help="number of blade elements")
parser.add_argument("NumElemTower", type=int, help="number of blade elements")

args = parser.parse_args()
NElem = args.NumElem
NElemT = args.NumElemTower

# Original Blades
R=63 # This is the original Value
A=np.genfromtxt('Blade.txt',delimiter=',',skip_header=0)
rR_ref=A[:,0]/R
cR_ref=A[:,1]/R
pitch_ref=A[:,2]
t2c_ref=A[:,3]
rR_New=np.linspace(rR_ref[0],rR_ref[-1],NElem)
cR_New=np.interp(rR_New,rR_ref,cR_ref)
pitch_New=np.interp(rR_New,rR_ref,pitch_ref)
t2c_New=np.interp(rR_New,rR_ref,t2c_ref)
for i in range(NElem):
    if(rR_New[i]<63/R):
        t2c_New[i]=0.18        
    if(rR_New[i]<40.45/R):
        t2c_New[i]=0.25        
    if(rR_New[i]<32.25/R):
        t2c_New[i]=0.25        
    if(rR_New[i]<24.05/R):
        t2c_New[i]=0.3        
    if(rR_New[i]<19.95/R):
        t2c_New[i]=0.35        
    if(rR_New[i]<15.85/R):
        t2c_New[i]=0.4        
    if(rR_New[i]<11.75/R):
        t2c_New[i]=1.        
    if(rR_New[i]<5.60/R):
        t2c_New[i]=2.        

L=91.5 # This is the original Value
B=np.genfromtxt('Tower.txt',delimiter=',')
rR_Tref=B[:,0]/L
cR_Tref=B[:,1]/L
pitch_Tref=B[:,2]
t2c_Tref=B[:,3]
rR_TNew=np.linspace(rR_Tref[0],rR_Tref[-1],NElemT)
cR_TNew=np.interp(rR_TNew,rR_Tref,cR_Tref)
pitch_TNew=np.interp(rR_TNew,rR_Tref,pitch_Tref)
t2c_TNew=np.interp(rR_TNew,rR_Tref,t2c_Tref)
#plt.figure(1)
#plt.plot(rR_New,cR_New,'b')
#plt.plot(rR_ref,cR_ref,'r')
#plt.show()
with open('NRELBlade_N'+str(NElem)+'.al','w') as fout:
    fout.write('R  : '+str(R)+' \n')
    fout.write('Spanwise  : 0.0 0.0 1.0 \n')
    fout.write('NStations : '+str(NElem)+'\n')
    for j in range(0,NElem):
        fout.write(str(rR_New[j])+'\t'+str(cR_New[j])+'\t'+str(pitch_New[j])+'\t'+str(t2c_New[j])+'\n')

with open('NRELTower_N'+str(NElemT)+'.al','w') as fout:
    fout.write('Length  : '+str(L) +'\n')
    fout.write('Spanwise  : 0.0 -1.0 0.0 \n')
    fout.write('NStations : '+str(NElemT)+'\n')
    for j in range(0,NElemT):
        fout.write(str(rR_TNew[j])+'\t'+str(cR_TNew[j])+'\t'+str(pitch_TNew[j])+'\t'+str(t2c_TNew[j])+'\n')

