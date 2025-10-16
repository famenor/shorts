import sys
sys.path.append('/home/armando/git/shorts/dimensional')

import numpy as np
import pandas as pd
from lib.data_profiler.data_profiler import ArrayProfiler

def test_profile_float_field():
    profiler = ArrayProfiler()
    float_array = pd.Series(np.array([1.1, 2.2, 3.3, 4.4, 5.5], dtype=float))
    
    result = profiler.profile_float_field(float_array)
    
    assert result['mean'] == np.mean(float_array)
    assert result['min'] == np.min(float_array)
    assert result['max'] == np.max(float_array)

def test_profile_string_field():
    profiler = ArrayProfiler()
    string_array = pd.Series(np.array(['a', 'b', 'a', 'c', 'b'], dtype=str))
    
    result = profiler.profile_string_field(string_array)
    
    assert result['unique_count'] == len(set(string_array))
    assert sorted(result['unique_values']) == sorted(list(set(string_array)))
