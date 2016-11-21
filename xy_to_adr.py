#!/usr/bin/python3
#-*- coding: utf-8 -*-
import sle_cache_lib as cache

idx=cache.Array_ref_lin()
idx.array_size=[512, 512]
idx.read('res/idx_1')
idx.run(0)
idx.save('res/addr_1')

