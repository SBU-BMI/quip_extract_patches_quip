import json
import PIL.ImageDraw as ImageDraw
import PIL.Image as Image
import glob
import collections
import openslide
import os
import pdb
import multiprocessing as mp
from user_setup_and_utils import *

settings = import_settings()

classes = settings['classes']
colors = settings['colors']
annots_fol = settings['annotation_fol']
wsi_fol = settings['wsi_fol']
out_fol = settings['mask_fol']
creators = settings['creators']

create_fol_if_not_exist(out_fol)
class_colors = {classes[i]:colors[i] for i in range(len(colors))}

manifest = [f.rstrip().split(',') for f in open(annots_fol + '/manifest.csv')]
fn_to_slideID = {fn.replace("\"", ""):slideID.split('/')[-1].replace("\"", "") for _, _, _, _, _, slideID, fn in manifest[1:]}

numWSINotFound = 0

def process_json(fn):
    slideID = fn_to_slideID[fn.split('/')[-1]]
    slide_path = os.path.join(wsi_fol, slideID)

    if not os.path.exists(slide_path):
        print('WSI not found: ================', slideID)
        numWSINotFound += 1
        return

    oslide = openslide.OpenSlide(slide_path)
    width, height = oslide.level_dimensions[5]      # extract the width and height at level 5

    print(fn, slide_path, width, height)
    data = json.load(open(fn))
    if len(data) == 0:
        return

    image = Image.new("RGB", (width, height))
    draw = ImageDraw.Draw(image)

    numValidRegions = 0
    for region in data:
        if 'creator' not in region:
            continue
        creator = region['creator']
        if len(creators) > 0 and (creator not in creators):
            print('Skip this creator: ', creator)
            continue

        coors = region['geometries']['features'][0]['geometry']['coordinates'][0]
        coors_converted = [(int(x*width), int(y*height)) for x, y in coors]
        if 'notes' not in region['properties']['annotations']: continue
        annot_type = region['properties']['annotations']['notes']

        if annot_type not in class_colors: continue
        draw.polygon(coors_converted, fill=class_colors[annot_type])
        numValidRegions += 1

    if numValidRegions > 0:
        image.save(os.path.join(out_fol, slide_path.split('/')[-1][:-4] + '.png'))

if __name__ == '__main__':
    fns = glob.glob(annots_fol + '/*.json')
    pool = mp.Pool(processes=20)
    pool.map(process_json, fns)
    pool.close()
