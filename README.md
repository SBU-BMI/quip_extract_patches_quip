# quip_extract_patches_quip
This repo contains codes that extract patches from WSIs given the annotations downloaded from QUIP.

### Change parameter settings
Change the parameters in user_setup_and_utils.py accordingly.

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
