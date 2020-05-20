import os

# change these settings accordingly

classes = ['Prostate-Benign', 'Prostate-Gleason 3', 'Prostate-Gleason 4', 'Prostate-Gleason 5-Single Cells', 'Prostate-Gleason 5']
colors = [(255, 0, 0), (255, 127, 0), (0, 0, 255), (255, 255, 255), (255, 255, 0)]
annotation_fol = '/data10/shared/hanle/extract_prostate_seer_john_grade5_subtypes/SEER-Rutgers-Prostate-2020-2-14'
svs_fol = '/data10/shared/hanle/svs_SEER_PRAD'
svs_extension = 'tif'

mask_fol = 'json_to_image/'
coordinate_fol = 'corrs_to_extract'
patches_fol = 'patches'
creators = {'32', '49'}     # 32 for  john.vanarnam; 49 for vanarnam3


mag_at_extraction = 20
patch_size_ROI = 200    # patch size of the ROI
patch_size_extracted = 200
level = 0

settings = {'classes':classes, 'colors':colors, 'annotation_fol':annotation_fol, 'svs_fol':svs_fol, 'mask_fol':mask_fol, 'coordinate_fol':coordinate_fol, 'patches_fol':patches_fol, 'creators':creators, 'svs_extension':svs_extension, 'mag_at_extraction':mag_at_extraction, 'patch_size_ROI':patch_size_ROI, 'patch_size_extracted':patch_size_extracted, 'level':level}


def import_settings():
    return settings

def create_fol_if_not_exist(fol):
    if not os.path.exists(fol):
        os.mkdir(fol)
    os.system('rm -rf {}/*'.format(fol))
