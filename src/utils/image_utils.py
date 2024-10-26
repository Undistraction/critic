import numpy as np
from skimage import io

# ------------------------------------------------------------------------------
# Exports 
# ------------------------------------------------------------------------------

def load_image(image_url):
    """Load an image from the supplied URL."""
    try:
        image = io.imread(image_url)
        # Normalize pixel values to [0, 1]
        return np.array(image, dtype=np.float64) / 255
    except FileNotFoundError:
        raise FileNotFoundError(f"Image file not found at '{image_url}'") 
    
    