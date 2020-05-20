import os
import sys
import glob
import collections
import random
import multiprocessing as mp

def process(data):
    i, fn = data
    cmd = 'cp ' + fn + ' ' + os.path.join(out_fol, str(i + 1) + '.png')
    os.system(cmd)

if __name__ == '__main__':
    classes = {'2':'grade4', '5':'grade5'}
    samples_per_slide = {'2':16, '5':250}
    out = []
    grade5_slides = {'001738-000316', '001738-000324', '001738-000325', '001738-000532'}
    out_fol = 'patches_prostate_seer_john_grade4_grade5_650_20X_samples_1000each'
    if not os.path.exists(out_fol):
        os.mkdir(out_fol)

    for current_class in classes.keys():
        number_patches_per_slide = samples_per_slide[current_class]

        fns = [f for f in glob.glob('patches_prostate_seer_john_grade4_grade5_650_20X/*' + current_class + '.png')]
        print('process class: ', classes[current_class], len(fns))
        maps = collections.defaultdict(list)

        for fn in fns:
            #folder/001738-100046-multires.tif_62234_40913_576_400_0.png
            slide_id = fn.split('/')[-1].split('.')[0]
            if fn[-5] == '5' and slide_id[:13] not in grade5_slides:
                continue
            maps[slide_id].append(fn)

        print('number of slides: ', len(maps))
        for _, fn in maps.items():
            random.shuffle(fn)
            out.extend(fn[:number_patches_per_slide])
        print('len of out: ', len(out))

    out = [(i, fn) for i, fn in enumerate(out)]
    pool = mp.Pool(processes = 32)
    pool.map(process, out)
    pool.close()

    with open(out_fol + '/label.txt', 'w') as f:
        for i, fn in out:
            f.writelines('{} {}\n'.format(i + 1, fn))
