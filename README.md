# quip_extract_patches_quip
This repo contains codes that extract patches from WSIs given the annotations downloaded from QUIP.

### Change parameter settings
Change the parameters in user_setup_and_utils.py accordingly.
All the basic parameters are found in user_setup_and_utils.py
The label of each class is the index of that class in parameter classes.
For example, if classes = ['Prostate-Benign', 'Prostate-Gleason 3'], then the label of "Prostate-Benign" is 0, "Prostate-Gleason 3" is 1

### Convert json annotations to png masks

- Run "python 1_json_parser.py"
- Output is png masks stored in mask_fol (a parameter in user_setup_and_utils.py)

### Extract coordinates of patches from the masks

- Run "python 2_masks_to_patches_coordinates.py"
- Output is .txt files with the format "WSI_name x_top_left y_top_left label"

### Extract patches from WSIs

- Run "python 3_extract_patches_from_WSIs.py"
- Output is patches stored in patches_fol
- Patches' filename has the format: ${WSI_name}\_${x_top_left}\_${y_top_left}\_${patch_size_at_highest_mag}\_${patch_size_at_stored_mag}\_${label}.png

e.g, 001738-000118-multires.tif_3457_12389_288_200_0.png
- ${WSI_name} = 001738-000118-multires.tif
- ${x_top_left} = 3457
- ${y_top_left} = 12389
- ${patch_size_at_highest_mag} = 288  # this is at 28X
- ${patch_size_at_stored_mag} = 200   # this is at 20X
- ${label} = 0
