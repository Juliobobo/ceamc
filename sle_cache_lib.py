#!/usr/bin/python3
#-*- coding: utf-8 -*-
import sys
import os
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


'''
bibliotheque pour la simulation de cache
Quatre classes :
 Cache         : pour lancer le simulateur de cache
 Array_ref_lin : transforme index en adresses, loi lineaire
 Array_ref_OBL : transforme index en adresses, loi par blocs pour OBL
 Rotate_run    : lance le programme rotation
 Experience    : lance les experiences
'''
###################################
class Cache:
    ''' 
    To simulate a cache 
    '''
    def __init__(self):
    # Default cache parameter
        self.name='cache'
        self.size=64*1024
        self.line_size=64
        self.associativity=2
        self.dta='res/din_data'

    def run(self, ref):
        dinarg='-informat d ' + \
            ' -l1-dsize ' + str(self.size) +\
            ' -l1-dbsize ' + str(self.line_size) + \
            ' -l1-dassoc ' + str(self.associativity) + \
            ' < ' + self.dta +\
            ' > res/din_res'

        fw=open(self.dta, 'w')
        for d in ref:
            fw.write('0 ' + str(d) + '\n')
        fw.close()
        ## run dinero and get result
        os.system('d4-7/dineroIV ' + dinarg)
        fr=open('res/din_res', 'r')
        self.nd=0
        self.miss=0
        self.totalb=0
        for l in fr:
            l=l.strip()
            if l.startswith('Demand Fetches'):
                r=l.split()
                self.nd=int(r[2])
            if l.startswith('Demand miss rate'):
                r=l.split()
                self.miss=float(r[3])
            if l.startswith('Total Bytes'):
                r=l.split()
                self.totalb=int(r[4])
        #print('nd ' + str(self.nd)+ ' ' +\
        #      'miss ' + str(self.miss) + ' ' +\
        #      'tb ' + str(self.totalb))
        fr.close()

##################################
class Array_ref_lin:
    '''
    To manage array references
    '''

    def __init__(self):
        self.array_size=[512, 512]
        
    def run(self,idx):
        if idx:
            self.idx=idx
            
        self.addr=[]
        n=[1,]+self.array_size[0:-1]
        o=[0.5]*len(self.array_size)
        o=np.multiply(self.array_size, o)
        offset=int(sum(np.multiply(o, n)))
        for i in self.idx:
            self.addr.append(sum(np.multiply(i, n))+offset)

    def read(self, name):
        self.idx=[]
        fr=open(name, 'r')
        for l in fr:
            self.idx.append(map(int,l.split(' ')))
        fr.close()
        
    def save(self, name):
        fw=open(name, 'w')
        for d in self.addr:
            fw.write(str(d) + '\n')
        fw.close()
        
###############################
class Array_ref_OBL:
    '''
    To manage array references
    '''
    def __init__(self):
        self.array_size=[512, 512]
        self.OBL_tile=[8,8]

    def run(self,idx):
        self.addr=[]
        for i in idx:
            ### A MODIFIER 
            self.addr.append(0)
            ### ATTENTION NUL PAR DEFAUT

############################
class Rotate_run:
    '''
    Launch the rotate program
    '''
    def __init__(self):
        self.array_size=[512, 512]
        self.tile_size=[16, 16]
        self.alpha=0.34
        self.fr='rtmp'
        
    def run(self):
        rotate_arg=' '.join(map(str,self.array_size + self.tile_size))+ ' ' +\
        str(self.alpha)
        os.system('rotation ' + rotate_arg + ' > res/idx')
        ## launch rotate rotate_arg > self.fr
        ## read idx
        self.idx=[]
        fr=open('res/idx', 'r')
        for l in fr:
            self.idx.append(map(int,l.split(' ')))
        fr.close()    
        #print(self.idx)    
            
#############################################
class Experience:
    ''' 
    Run an experience 
    '''
    def __init__(self):
        # Config par defaut
        self.tile_step=1
        self.tile_max=16
        self.array_size=[512,512]
        self.plot_name='miss_rate.pdf'

        self.app=Rotate_run()
        self.idx=Array_ref_lin()
        self.cache=Cache()

    def setup(self):
        self.app.array_size=self.array_size
        self.idx.array_size=self.array_size
        
    def run(self):
        self.setup()
        self.t=range(1,self.tile_step)+range(self.tile_step,
                                             self.tile_max+self.tile_step,
                                             self.tile_step)
        self.r=[]
        self.tb=[]
        # Lance les simus et conserve taux de defaut
        for ts in self.t:
            print('tile size : ' + str(ts))
            self.app.tile_size=[ts, ts]
            self.app.run()
            self.idx.run(self.app.idx)
            self.cache.run(self.idx.addr)
            # Enregistre mesures
            self.r.append(self.cache.miss)
            self.tb.append(self.cache.totalb)
        print('miss rate : ' + str(self.r))
        print('total qty : ' + str(self.tb))

    def plot(self):
        fig = plt.figure(1)
        ax = fig.add_subplot(111)
        ax.axis([0,self.t[-1]+1,0,1.0])
        plt.title('Miss rate')
        plt.ylabel('Miss rate')
        plt.xlabel('Tile Size')
        ax.plot(self.t, self.r)
        fig.savefig(self.plot_name)
        figq = plt.figure(2)
        axq = figq.add_subplot(111)
        axq.axis([0,self.t[-1]+1,0,1.1*max(self.tb)])
        plt.title('Qty')
        plt.ylabel('Qty')
        plt.xlabel('Tile Size')
        axq.plot(self.t, self.tb)
        if os.path.dirname(self.plot_name):
            nm=os.path.dirname(self.plot_name)+'/q_'+os.path.basename(self.plot_name)
        else:
             nm='q_'+os.path.basename(self.plot_name)
        figq.savefig(nm)
        # Ajouter nbre bytes chargés

