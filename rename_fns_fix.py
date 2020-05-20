import os
import sys
import multiprocessing as mp

fol = sys.argv[1]   #sample_micropap_5000
fns_old = [f.rstrip().split() for f in open(os.path.join(fol, 'label_new.txt'), 'r')]
fns_old = {fn[0]:fn[2] for fn in fns_old}

fns_new = [f.rstrip().split() for f in open(os.path.join(fol, 'label_new_fix.txt'), 'r')]
fns_new = [[fns_old[id], id, fn] for id, _, fn in fns_new if int(id) >= 5000]

def process(fn):
    cur_fn, _, new_fn = fn
    cmd = 'mv ' + os.path.join(fol, cur_fn) + ' ' + os.path.join(fol, new_fn)
    print(cmd)
    os.system(cmd)

pool = mp.Pool(processes=60)
pool.map(process, fns_new)

