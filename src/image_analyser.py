from arrow import get
import numpy as np
import typing
from sklearn.cluster import KMeans
from sklearn.utils import shuffle
from skimage import color
from src.utils.color_utils import discard_transparency, get_frequency_ratios, lab_sort_by_frequency, lab_to_all, lab_to_hex_array, lab_to_rgb_array, lab_sort_by_hue

# ------------------------------------------------------------------------------
# Const 
# ------------------------------------------------------------------------------

SWATCH_HEIGHT = 50
SAMPLE_SIZE = 2000
RANDOM_STATE = 0

# ------------------------------------------------------------------------------
# Utils 
# ------------------------------------------------------------------------------

def get_colors_sorted_by_hue(lab_colours): 
  """Sort an array of LAB colors by their hue component."""
  lab_colors_sorted = lab_sort_by_hue(lab_colours)
  return lab_to_all(lab_colors_sorted) 
  
def get_colors_sorted_by_frequency(lab_colours, labels):
  """Sort an array of LAB colors by the size of their clusters"""
  lab_colors_sorted = lab_sort_by_frequency(lab_colours, labels)
  return lab_to_all(lab_colors_sorted)
  
# ------------------------------------------------------------------------------
# Exports 
# ------------------------------------------------------------------------------

def cluster_colors(image, n_colors):
  """Use k-means clustering to cluster the colors in the image."""
  # Convert the image from RGB to LAB color space. LAB gives us a colour space
  # that better matches the way humans see colours. 
  image_lab = color.rgb2lab(image)

  # Reshape the image data from a nested to a flat array for processing
  w, h, d = image_lab.shape
  image_array = np.reshape(image_lab, (w * h, d))

  # Get a random sample of the image data (we don't need all of it to fit the
  # model and a sample is much faster)
  image_array_sample = shuffle(image_array, random_state=RANDOM_STATE)[:SAMPLE_SIZE]
  # Train the model using the sample data
  kmeans = KMeans(n_clusters=n_colors, random_state=RANDOM_STATE).fit(image_array_sample)
  # Use the model to assign all the pixels in the image to a cluster
  labels = kmeans.predict(image_array)
  
  return kmeans, labels, (w,h,d)

def analyse_image(image, n_colors):
  """Analyse the image for its color palette."""
  image_without_transparency = discard_transparency(image)
  # Cluster the colors using k-means
  kmeans, labels, whd = cluster_colors(image_without_transparency, n_colors)
  lab_colours = kmeans.cluster_centers_
  # Sort
  by_hue = get_colors_sorted_by_hue(lab_colours)
  by_frequency = get_colors_sorted_by_frequency(lab_colours, labels)
  
  result = {
    'colors': {
      'meta': {
        'frequencyRatios': get_frequency_ratios(lab_colours, labels),
      },
      'sorted': {
        'by_hue': by_hue,
        'by_frequency': by_frequency
      },
    }
  }
  
  return result
