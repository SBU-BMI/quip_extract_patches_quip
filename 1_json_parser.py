import json
import PIL.ImageDraw as ImageDraw
import PIL.Image as Image
import glob
import collections
import openslide
import os
import pdb
import multiprocessing as mp

classes = ['Prostate-Benign', 'Prostate-Gleason 3', 'Prostate-Gleason 4', 'Prostate-Gleason 5-Single Cells', 'Prostate-Gleason 5-Secretions', 'Prostate-Gleason 5']
colors = [(255, 0, 0), (255, 127, 0), (0, 0, 255), (255, 255, 255), (139, 0, 255), (255, 255, 0)]

classes = ['Prostate-Benign', 'Prostate-Gleason 3', 'Prostate-Gleason 4', 'Prostate-Gleason 5-Single Cells', 'Prostate-Gleason 5']
colors = [(255, 0, 0), (255, 127, 0), (0, 0, 255), (255, 255, 255), (255, 255, 0)]


color_codes = {classes[i]:colors[i] for i in range(len(colors))}
annots_fol = 'SEER-Rutgers-Prostate-2020-2-14'

#included_slides = {'001738-000145', '001738-000138', '001738-000179', '001738-000193', '001738-000221', '001738-000268', '001738-000265', '001738-000275', '001738-000032', '001738-000033', '001738-000031', '001738-000316', '001738-000324', '001738-000325', '001738-000532'}

annot_types = collections.defaultdict(int)
manifest = [f.rstrip().split(',') for f in open(annots_fol + '/manifest.csv')]
fn_to_slideID = {fn.replace("\"", ""):slideID.split('/')[-1].replace("\"", "") for _, _, _, _, _, slideID, fn in manifest[1:]}
svs_fol = '/data10/shared/hanle/svs_SEER_PRAD'
svs_fol2 = ''
svs_fol3 = ''
svs_fols = [svs_fol, svs_fol2, svs_fol3]

john_creators = {'32', '49'}  # 32 for  john.vanarnam; 49 for vanarnam3
notes = collections.defaultdict(int)
numWSINotFound = 0

def isFileExists(folder, slideID):
    slide_path = os.path.join(folder, slideID)
    if os.path.exists(slide_path):
        return True
    return False

def process_json(fn):
    slideID = fn_to_slideID[fn.split('/')[-1]]
    slide_path = None
    for fol in svs_fols:
        if isFileExists(fol, slideID):
            slide_path = os.path.join(fol, slideID)
            break
    if slide_path is None:
        print('WSI not found: ================', slideID)
        numWSINotFound += 1
        return

    #if slideID[:13] not in included_slides:
    #    return

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
        if creator not in john_creators:
            continue

        coors = region['geometries']['features'][0]['geometry']['coordinates'][0]
        coors_converted = [(int(x*width), int(y*height)) for x, y in coors]
        if 'notes' not in region['properties']['annotations']: continue
        annot_type = region['properties']['annotations']['notes']

        notes[annot_type] += 1
        if annot_type not in color_codes: continue
        draw.polygon(coors_converted, fill=color_codes[annot_type])
        numValidRegions += 1

    if numValidRegions > 0:
        image.save('json_to_image/' + slide_path.split('/')[-1][:-4] + '.png')


fns = glob.glob(annots_fol + '/*.json')
pool = mp.Pool(processes=64)
pool.map(process_json, fns)
pool.close()
print(notes)
