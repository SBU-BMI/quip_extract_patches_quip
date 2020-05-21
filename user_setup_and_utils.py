import os

# change these settings accordingly

# name of classes in the annotations
classes = ['Prostate-Benign', 'Prostate-Gleason 3', 'Prostate-Gleason 4', 'Prostate-Gleason 5-Single Cells', 'Prostate-Gleason 5']
# color of the mask for each class
colors = [(255, 0, 0), (255, 127, 0), (0, 0, 255), (255, 255, 255), (255, 255, 0)]

# path to the annotation folder that is downloaded from QUIP
annotation_fol = '/data10/shared/hanle/extract_prostate_seer_john_grade5_subtypes/SEER-Rutgers-Prostate-2020-2-14'
# creator ID of the annotators
creators = {}     # '32' for  john.vanarnam; '49' for vanarnam3. If creators == {}: use everyone's annotations.

# maximum number of patches per class per slide to be extracted
# if max_patches_per_class_per_wsi = -1 then extract all posible patches, non-overlap
max_patches_per_class_per_wsi = -1

# path to WSI folder
wsi_fol = '/data10/shared/hanle/svs_SEER_PRAD'
# extention of WSI in the wsi_fol
wsi_extension = 'tif'

# folder that contains the masks generated from annotations
mask_fol = 'json_to_image/'
# folder that contains .txt files that contain coordinates of patches
coordinate_fol = 'corrs_to_extract'
# folder that contain extracted patches
patches_fol = 'patches'

# magnification at which the patches are stored
mag_at_extraction = 20
# the patch size of the ROI, the label of ROI is decided by the corresponding mask regions. Patches are saved at mag_at_extraction magnification
patch_size_ROI = 200
# the patch size that will be extracted, patch_size_extracted >= patch_size_ROI. when patch_size_extracted > patch_size_ROI, it contains the surrounding area
patch_size_extracted = 200
# the level of WSIs where the patches are extracted. level = 0 is the highest magnification
level = 0


settings = {'classes':classes, 'colors':colors, 'annotation_fol':annotation_fol, 'wsi_fol':wsi_fol, 'mask_fol':mask_fol, 'coordinate_fol':coordinate_fol, 'patches_fol':patches_fol, 'creators':creators, 'wsi_extension':wsi_extension, 'mag_at_extraction':mag_at_extraction, 'patch_size_ROI':patch_size_ROI, 'patch_size_extracted':patch_size_extracted, 'level':level, 'max_patches_per_class_per_wsi':max_patches_per_class_per_wsi}


def import_settings():
    return settings

def create_fol_if_not_exist(fol):
    if not os.path.exists(fol):
        os.mkdir(fol)
    os.system('rm -rf {}/*'.format(fol))
