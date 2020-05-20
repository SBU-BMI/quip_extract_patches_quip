import numpy as np
import openslide
import sys
import os
from PIL import Image
import datetime
import time
import cv2
from shutil import copyfile as cp
import multiprocessing as mp
from user_setup_and_utils import *

settings = import_settings()
svs_fol = settings['svs_fol']
corr_fol = settings['coordinate_fol']
output_folder = settings['patches_fol']
create_fol_if_not_exist(output_folder)

patch_size_extracted = settings['patch_size_extracted']
mag_at_extraction = settings['mag_at_extraction']
offset_to_top_left = 0  # an extra setting to extract surrounding area
level = settings['level']

slide_corrs = [f for f in os.listdir(corr_fol) if 'txt' in f]
print(slide_corrs)

def extract_svs(fn):
    print('Processing... ', fn)
    slide = fn[:-4]

    slide_path = os.path.join(svs_fol, slide)
    if not os.path.exists(slide_path):
        print('file not found: ', slide)
        return

    try:
        oslide = openslide.OpenSlide(slide_path);
        if openslide.PROPERTY_NAME_MPP_X in oslide.properties:     # 'openslide.mpp-x'
            mag = 10.0 / float(oslide.properties[openslide.PROPERTY_NAME_MPP_X]);
        elif "XResolution" in oslide.properties:
            mag = 10.0 / float(oslide.properties["XResolution"]);
        elif 'tiff.XResolution' in oslide.properties:   # for Multiplex IHC WSIs, .tiff images
            Xres = float(oslide.properties["tiff.XResolution"])
            if Xres < 10:
                mag = 10.0 / Xres;
            else:
                mag = 10.0 / (10000/Xres)       # SEER PRAD
        else:
            print('[WARNING] mpp value not found. Assuming it is 40X with mpp=0.254!', slide);
            mag = 10.0 / float(0.254);
        pw = int(patch_size_extracted * mag / mag_at_extraction);
        pw_offset = int(offset_to_top_left * mag / mag_at_extraction)

        width = oslide.dimensions[0];
        height = oslide.dimensions[1];
    except:
        print('{}: exception caught'.format(slide));
        exit(1);

    corrs = [x.split()[1:] for x in open(os.path.join(corr_fol, fn))]

    for x, y, lb in corrs:
        x, y = int(x) - pw_offset, int(y) - pw_offset

        if x < 0 or x < 0: continue
        fname = '{}/{}_{}_{}_{}_{}_{}.png'.format(output_folder, slide, x, y,\
                pw + 2*pw_offset, 2*offset_to_top_left + patch_size_extracted, lb)
        patch = oslide.read_region((int(x), int(y)), 0, (pw + 2*pw_offset, pw + 2*pw_offset));
        patch_arr = np.array(patch);
        wh = (np.std(patch_arr[:,:,0].flatten()) + np.std(patch_arr[:,:,1].flatten()) + np.std(patch_arr[:,:,2].flatten())) / 3.0
        if(patch_arr[:,:,3].max() == 0 or wh <= 12):
            continue

        patch = patch.resize((int(patch_size_extracted + 2*offset_to_top_left), int(patch_size_extracted + 2*offset_to_top_left)), Image.ANTIALIAS);
        patch.save(fname);


if __name__ == '__main__':
    start = time.time()
    pool = mp.Pool(processes=20)
    pool.map(extract_svs, slide_corrs)
    print('Elapsed time: ', (time.time() - start)/60.0)

