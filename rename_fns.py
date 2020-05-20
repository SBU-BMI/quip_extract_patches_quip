import os
import sys
import multiprocessing as mp

fol = sys.argv[1]   #sample_micropap_5000
fns = [f.rstrip().split() for f in open(os.path.join(fol, 'label_new.txt'), 'r')]
#for cur_fn, _, new_fn in fns:
def process(fn):
    cur_fn, _, new_fn = fn
    cmd = 'mv ' + os.path.join(fol, cur_fn + '.png') + ' ' + os.path.join(fol, new_fn)
    print(cmd)
    os.system(cmd)

pool = mp.Pool(processes=60)
pool.map(process, fns)

