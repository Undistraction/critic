import colorspacious as cs
from matplotlib import scale
from skimage import color
import numpy as np
from src.utils.list_utils import nested_numpy_lists_to_list
import math

# ------------------------------------------------------------------------------
# Exports 
# ------------------------------------------------------------------------------

def scale_rgb(rgb_color):
    return round(rgb_color[0] * 255), round(rgb_color[1] * 255), round(rgb_color[2] * 255)

def lab_to_lch(lab):
    """Convert a LAB color to LCH (Lightness, Chroma, Hue)."""
    return cs.cspace_convert(lab, "CIELab", "CIELCh")

def get_cluster_indices_sorted_by_label_size(labels):
    """Get the indices of the clusters sorted by the size of their labels."""
    # Calculate the size of each cluster
    cluster_sizes = np.bincount(labels)
    # Sort by size in descending order
    sorted_indices = np.argsort(cluster_sizes)[::-1] 
    return sorted_indices


def get_frequency_ratios(lab_colors, labels):
    """Get the frequency of each color in the image."""
    # Calculate the size of each cluster
    cluster_sizes = np.bincount(labels)
    # Sort by size in descending order
    indices_sorted = np.argsort(cluster_sizes)[::-1] 
    # Reorder cluster sizes
    cluster_sizes_sorted = cluster_sizes[indices_sorted]
    print('@csizes', cluster_sizes_sorted)
    # Calculate the frequency of each color
    frequency_ratios = cluster_sizes_sorted / len(labels)
    print('@ratios', frequency_ratios)
    # Convert to a list of dictionaries
    return list(frequency_ratios)

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
    indices = get_cluster_indices_sorted_by_label_size(labels)
    return nested_numpy_lists_to_list(lab_colors[indices])

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
    # Check if there is an alpha channel (r,g,b,a)
    if image.shape[-1] == 4:
        image = np.asarray(image)
    
        # Flatten to 2D array of pixels
        pixels = image.reshape(-1, 4)
        
        # Filter out the pixels with an alpha value of less than 1
        alpha_mask = np.isclose(pixels[:, 3], 1.0)
        valid_pixels = pixels[alpha_mask]
        
        # Get RGB values
        rgb_pixels = valid_pixels[:, :3]
        
        # Calculate dimensions for roughly square image
        num_pixels = len(rgb_pixels)
        width = int(math.sqrt(num_pixels))
        height = num_pixels // width
        
        # Adjust width and height to fit all pixels. Changing the shape of the
        # image doesn't matter as we are only interested in the colors, but to
        # return an image it does need to have a full matrix of pixels.
        while width * height < num_pixels:
            width += 1
            height = num_pixels // width
        
        # Reshape array
        result = rgb_pixels[:width*height].reshape(height, width, 3)
        
        return result
    
    return image