from enum import Enum

# Use this file to adjust simulation settings.

# PyChrono Datapath. Past yours here
DATAPATH = "C:\\ProgramData\\Anaconda3\\Library\\data\\"

# Generation loop settings
NUM_TRIALS = 1
MAX_GEN = 50  # maximum number of generations the exp runs for
POPULATION_SIZE = 50
EXP_NAME = "adaptive_shaking_fixed" + "_pop" + str(POPULATION_SIZE) + "_gen" + str(MAX_GEN)

# Display settings
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
# Default: 0.5, 0.5, 1.0
CAMERA_X = 3.5  # Zoomed out: 3.5 3.5 5.0
CAMERA_Y = 10
CAMERA_Z = 5
DISPLAY_TIME = 20  # seconds (used for visualize_solution.py)

# SIMULATION Settings
SPEED = 0.005
SHOULD_VISUALIZE = True
SIMULATION_RUNTIME = 6  # seconds
BLOCK_X_POS = 0
BLOCK_Z_POS = 0
NUM_BLOCKS = 4
# default values for FREQ_X and AMP_X are 1.5 and 0.12
TABLE_FREQ_X = 1.5
TABLE_AMP_X = .12  # custom: freq=1.5 , amp =0.0005
# default value for FREQ_Y and AMP_Y are 1.5 and 0.001
TABLE_FREQ_Y = 1.5
TABLE_AMP_Y = .0005
# default value for FREQ_Z and AMP_Z are 1.5 and 0.12
TABLE_FREQ_Z = 1.5
TABLE_AMP_Z = .12

# Constraints
BLOCK_VOLUME = 0.0036
BLOCK_MASS = 3.6
STRUCTURE_MASS = BLOCK_MASS * NUM_BLOCKS
CANCEL_SIM_THRESHOLD = pow(BLOCK_VOLUME, 1 / 3)
MIN_DIMENSIONS_THRESHOLD = pow(BLOCK_VOLUME, 1 / 3) / 8

# Fitness thresholds for changing the environment.
FITNESS_INTERVAL = 400
INIT_ENV_LEVEL = 1
SHAKE_IN_X_AXIS_LEVEL = 2
SHAKE_IN_X_AND_Z_AXIS_LEVEL = 3

# used for the visualization file

SEED = 5


# Enum for Fitness Functions
class Fitness(Enum):
    SumLengths = "SumLengths"
    MaxPosition = "MaxPosition"
    MaxPositionSumLengths = "MaxPositionSumLengths"


# Setting the Fitness Function
FITNESS_FUNCTION = Fitness.SumLengths
