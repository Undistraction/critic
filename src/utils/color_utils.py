import colorspacious as cs
from matplotlib import scale
from skimage import color
import numpy as np
from src.utils.list_utils import nested_numpy_lists_to_list

# ------------------------------------------------------------------------------
# Exports 
# ------------------------------------------------------------------------------

def scale_rgb(rgb_color):
    return round(rgb_color[0] * 255), round(rgb_color[1] * 255), round(rgb_color[2] * 255)

def lab_to_lch(lab):
    """Convert a LAB color to LCH (Lightness, Chroma, Hue)."""
    return cs.cspace_convert(lab, "CIELab", "CIELCh")

def lab_sort_by_hue(lab_colors):
    """Sort an array of LAB colors by their hue component."""
    lch_colors = [lab_to_lch(lab) for lab in lab_colors]
    # Extract hue values and sort by hue
    sorted_lch_colors = sorted(lch_colors, key=lambda lch: lch[2])
    # Convert back to LAB
    sorted_lab_colors = [cs.cspace_convert(lchColor, "CIELCh", "CIELab") for lchColor in sorted_lch_colors]
    return nested_numpy_lists_to_list(sorted_lab_colors)

def lab_sort_by_frequency(lab_colors, labels):
    """Sort an array of LAB colors by the size of their clusters."""
    # Calculate the size of each cluster
    cluster_sizes = np.bincount(labels)
    
    # Sort by size in descending order
    sorted_indices = np.argsort(cluster_sizes)[::-1]  
    return nested_numpy_lists_to_list(lab_colors[sorted_indices])

def lab_to_hex(lab_color):
    """Convert a LAB color to a hex color."""
    rgb_color = color.lab2rgb(lab_color, illuminant='D65', observer='2')
    r = round(rgb_color[0] * 255)
    g = round(rgb_color[1] * 255)
    b = round(rgb_color[2] * 255)

    # Format up as hex string, i.e. #ECF0EF
    hex = f'#{r:02X}{g:02X}{b:02X}'
    return hex

def lab_to_hex_array(lab_colors):
    """Convert an array of LAB colors to an array of hex colors."""
    hex_colors = []
    for i, lab_color in enumerate(lab_colors):
        hex_color = lab_to_hex(lab_color)
        hex_colors.append(hex_color)
    return hex_colors

def lab_to_rgb_array(lab_colors):
    """Convert an array of LAB colors to an array of RGB (Red, Green, Blue) colors."""
    rgb_colors = []
    for i, lab_color in enumerate(lab_colors):
        # Convert the Lab color back to RGB for display
        rgb_color = color.lab2rgb(np.array([[lab_color]]), illuminant='D65', observer='2')[0][0]
        rgb_color_scaled = scale_rgb(rgb_color)
        rgb_colors.append(rgb_color_scaled)
    return rgb_colors

def lab_to_all(lab):
    """Create a dictionary containing the LAB, RGB, and hex representations of a color."""
    rgb = lab_to_rgb_array(lab)
    hex = lab_to_hex_array(lab)
    return {
        "lab": lab,
        "rgb": rgb,
        "hex": hex
    }

def discard_transparency(image):
    """If the image has an alpha channel, remove all pixels that have an alpha value greater than zero and discard all alpha channel data."""
    if image.shape[-1] == 4:
        # Create a mask for the transparent pixels
        opaque_mask = image[:, :, 3] == 0
        # Create a new RGB array for the result
        height, width = image.shape[:2]
        result = np.zeros((height, width, 3), dtype=image.dtype)

        # Copy RGB values for opaque pixels
        result[opaque_mask] = image[opaque_mask][:, :3]

        return result
    return image