#!/usr/bin/python3
#-*- coding: utf-8 -*-
import sle_cache_lib as cache


# Commence les mesures
print('go')
expe=cache.Experience()

# Premiere configuration
expe.cache.line_size=64
expe.cache.size=16*1024
expe.cache.associativity=64

expe.array_size=[512,512]
expe.tile_max=128
expe.tile_step=16
# lance experience avec angle de rotation 0
expe.app.alpha=1.57
expe.plot_name='res/expe_simple0.52.pdf'
expe.run()
expe.plot()
print('done')
#expe.app.alpha=0.52
#expe.plot_name='res/e2.pdf'
#expe.run()
#expe.plot()
#print('done')
# Exemple pour OBL
#expe.idx=cache.Array_ref_OBL()
#expe.idx.OBL_tile=[32, 2]
#expe.dta='res/e1_OBL.pdf'
#expe.run()
#expe.plot()
#print('done')
