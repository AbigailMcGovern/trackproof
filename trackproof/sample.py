import numpy as np
import pandas as pd

# Reinforcement learning to find boxes/tracks in which errors are found (+1 for every error identified possibly pentalty for correct segments)

# Input
#   Image & tracks or subsection (might be too computationally intensive to process the whole thing)

# Output:
#   chosen track segment