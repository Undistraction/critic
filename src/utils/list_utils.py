# ------------------------------------------------------------------------------
# Exports 
# ------------------------------------------------------------------------------

def nested_numpy_lists_to_list(nested_numpy_lists):
  """Convert a nested list of numpy arrays to a nested list of lists."""
  nested_lists = []
  for nested_list in nested_numpy_lists:
    nested_lists.append(nested_list.tolist())
  return nested_lists