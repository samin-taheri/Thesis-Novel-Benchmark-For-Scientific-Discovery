import random, numpy as np
def fix_seed(seed: int = 42):
    random.seed(seed)
    np.random.seed(seed)
