import os
import sys
import random
import multiprocessing as mp

def process(fn):
    i, fn = fn
    cmd = 'cp {} {}'.format(os.path.join(in_fol, fn), os.path.join(out_fol, str(i + 1) + '.png'))
    print(cmd)
    os.system(cmd)

if __name__ == '__main__':
    #in_fol = 'patches_lung_seer_john_mucinous'
    in_fol = sys.argv[1]

    out_fol = in_fol + '_web'
    if not os.path.exists(out_fol):
        os.mkdir(out_fol)

    no_of_samples = 12_000
    fns = [f for f in os.listdir(in_fol)]
    random.shuffle(fns)
    fns = fns[:max(len(fns), no_of_samples)]

    fid = open(os.path.join(out_fol, 'label.txt'), 'w')
    for i, fn in enumerate(fns):
        fid.writelines('{} {}\n'.format(i + 1, fn))
    fid.close()

    fns = [(i, fn) for i, fn in enumerate(fns)]
    pool = mp.Pool(processes=32)
    pool.map(process, fns)

