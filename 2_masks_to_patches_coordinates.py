import os
import sys
import numpy as np
import cv2
from PIL import Image
import openslide
import random
import multiprocessing as mp
import time
import pdb
from user_setup_and_utils import *

settings = import_settings()
classes = settings['classes']
colors = settings['colors']
wsi_fol = settings['wsi_fol']
input_mask_fol = settings['mask_fol']
out_fol = settings['coordinate_fol']
wsi_extension = settings['wsi_extension']

class_colors = {classes[i]:colors[i] for i in range(len(colors))}
class_ids = {classes[i]:i for i in range(len(classes))}
create_fol_if_not_exist(out_fol)


settings = {'classes':classes, 'colors':colors, 'annotation_fol':annotation_fol, 'wsi_fol':wsi_fol, 'mask_fol':mask_fol, 'coordinate_fol':coordinate_fol, 'patches_fol':patches_fol, 'creators':creators, 'wsi_extension':wsi_extension, 'mag_at_extraction':mag_at_extraction, 'patch_size_ROI':patch_size_ROI, 'patch_size_extracted':patch_size_extracted}

mag_at_extraction = settings['mag_at_extraction']
patch_size_ROI = settings['patch_size_ROI']
patch_size_extracted = settings['patch_size_extracted']
offset = int((patch_size_extracted - patch_size_ROI)/2)  # patch size that contains surrounding area for context purpose.

slide_ids = [fn for fn in os.listdir(input_mask_fol) if '.png' in fn]

def find_blobs(img, xScale=1.0, yScale=1.0, offset_to_top_left=0):
    print('shape of img: ', img.shape)
    img = img*255
    img = img.astype(np.uint8)
    kernel = np.ones((3,3), np.uint8)
    img = cv2.erode(img, kernel, iterations=1)

    # find contours in the binary image
    cnts = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    print('len of contours: ', len(cnts))
    if len(cnts) == 3:
        _, contours, _ = cnts
    else:
        contours, _ = cnts
    out = []
    for c in contours:
        # calculate moments for each contour
        M = cv2.moments(c)

        # calculate x,y coordinate of center
        if M["m00"] != 0:
            cX, cY = M["m10"] / M["m00"], M["m01"] / M["m00"]
            if cX - offset_to_top_left < 0 or cY - offset_to_top_left < 0:
                continue
            cX = int((cX - offset_to_top_left) * xScale)
            cY = int((cY - offset_to_top_left) * yScale)
            out.append((cY, cX))
    return out

def extract_patch(slide):
    annots_path = os.path.join(input_mask_fol, slide)
    annots = np.array(Image.open(annots_path).convert('RGB'))
    masks = {}
    for key, _ in class_colors.items():
        masks[key] = np.zeros(annots.shape[:2])

    slideID = slide[:-4] + '.' + wsi_extension

    slide_path = os.path.join(wsi_fol, slideID)
    if not os.path.exists(slide_path):
        print('file not found: ', slideID)
        return

    oslide = openslide.OpenSlide(slide_path)
    if openslide.PROPERTY_NAME_MPP_X in oslide.properties:
        mag = 10.0 / float(oslide.properties[openslide.PROPERTY_NAME_MPP_X])
    elif "XResolution" in oslide.properties:
        mag = 10.0 / float(oslide.properties["XResolution"])
    elif 'tiff.XResolution' in oslide.properties:  # for Multiplex IHC WSIs, .tiff images
        Xres = float(oslide.properties["tiff.XResolution"])
        if Xres < 10:
            mag = 10.0 / Xres
        else:
            mag = 10.0 / (10000 / Xres)  # SEER PRAD
    else:
        print('[WARNING] mpp value not found. Assuming it is 40X with mpp=0.254!', slide)
        mag = 10.0 / float(0.254);

    width = oslide.dimensions[0];
    height = oslide.dimensions[1];
    if abs(height / annots.shape[0] - width / annots.shape[1]) > 0.1:
        print('============================ERROR=================')
        return

    R, G, B = annots[:, :, 0], annots[:, :, 1], annots[:, :, 2]
    for key in masks.keys():
        cond = np.logical_and(R == class_colors[key][0], G == class_colors[key][1])
        cond = np.logical_and(cond, B == class_colors[key][2])
        masks[key][cond] = 1
        print(key, class_ids[key], class_colors[key], np.sum(masks[key]))
        sys.stdout.flush()

    corrs = {}
    for key in class_colors.keys():
        corrs[key] = []

    scale = height / annots.shape[0]
    pw_mask = int(patch_size_ROI * mag / mag_at_extraction / scale)
    offset_mask = int(offset * mag / mag_at_extraction / scale)
    threshold = 0.75
    for r in range(0, annots.shape[0] - pw_mask, pw_mask):
        for c in range(0, annots.shape[1] - pw_mask, pw_mask):
            for key in corrs.keys():
                if np.sum(masks[key][r:r + pw_mask, c:c + pw_mask]) > threshold * pw_mask * pw_mask:
                    if r - offset_mask < 0 or c - offset_mask < 0:
                        continue
                    corrs[key].append((int((r - offset_mask) * scale), int((c - offset_mask) * scale)))

    for key, val in corrs.items():
        random.shuffle(val)
        limit = 20
        corrs[key] = val[:min(limit, len(val))]

    offset_to_top_left = pw_mask / 2  + offset
    for key in corrs.keys():
        if np.sum(masks[key]) > 50:
            blob_y_x = find_blobs(masks[key], scale, scale, offset_to_top_left)
            corrs[key].extend(blob_y_x)

    corr_file = open(os.path.join(out_fol, slide[:-4] + '.' + wsi_extension + '.txt'), 'w')
    for key, val in corrs.items():
        for y, x in val:
            corr_file.writelines('{} {} {} {}\n'.format(slide.split('.')[0], x, y, class_ids[key]))

    corr_file.close()


if __name__ == '__main__':
    start = time.time()
    pool = mp.Pool(processes=20)
    pool.map(extract_patch, slide_ids)
    print('Elapsed time: ', (time.time() - start) / 60.0)
