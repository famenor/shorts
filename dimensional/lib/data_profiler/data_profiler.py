from abc import ABC, abstractmethod

import pandas as pd
import numpy as np

#ARRAY PROFILER DEFINITION
class AbstractArrayProfiler(ABC):
  
    @abstractmethod
    def profile_float_field(self, array) -> None:
        pass

    @abstractmethod
    def profile_string_field(self, array) -> None:
        pass

#ARRAY PROFILER IMPLEMENTATION
class ArrayProfiler(AbstractArrayProfiler):

    def __init__(self):
        pass

    def profile_float_field(self, array: pd.Series) -> None:
        result = {}
        result['mean'] = np.mean(array)
        result['min'] = np.min(array)
        result['max'] = np.max(array)
        return result

    def profile_string_field(self, array: pd.Series) -> None:
        result = {}
        result['unique_count'] = array.nunique()
        result['unique_values'] = array.unique().tolist()
        return result

#TABLE PROFILER DEFINITION
class AbstractTableProfiler(ABC):

    @abstractmethod
    def profile(self):
        pass

#TABLE PROFILER IMPLEMENTATION
class TableProfiler(AbstractTableProfiler):

    def __init__(self, table: pd.DataFrame):
        self.table = table
        self.array_profiler = ArrayProfiler()
     
    def profile(self, subset=None) -> dict:

        if subset is None:
            subset = self.table.columns

        profile = {}    
        for column in subset:

            if pd.api.types.is_float_dtype(self.table[column]):
                result = self.array_profiler.profile_float_field(self.table[column])
                profile[column] = result

            elif pd.api.types.is_string_dtype(self.table[column]):
                result = self.array_profiler.profile_string_field(self.table[column])
                profile[column] = result

        return profile
