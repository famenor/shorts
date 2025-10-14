from abc import ABC, abstractmethod

import pandas as pd
import numpy as np

#DATA PROFILER DEFINITION
class AbstractDataProfiler(ABC):

    def __init__(self, table: pd.DataFrame):
        self.table = table

    @abstractmethod
    def profile_float_field(self, field: str) -> None:
        pass

    @abstractmethod
    def profile_string_field(self, field: str) -> None:
        pass

#DATA PROFILER IMPLEMENTATION
class DataProfiler(AbstractDataProfiler):

    def profile_float_field(self, field: str) -> None:
        print('')
        print('Perfilando el campo: ' + field)
        print('Media: ' + str(np.mean(self.table[field])))
        print('Desviación estándar: ' + str(np.std(self.table[field])))
        print('Mínimo: ' + str(np.min(self.table[field])))
        print('Máximo: ' + str(np.max(self.table[field])))

    def profile_string_field(self, field: str) -> None:
        print('')
        print('Perfilando el campo: ' + field)
        print('Número de valores únicos: ' + str(self.table[field].nunique()))
        print('Valores únicos: ' + str(self.table[field].unique()))

#DATA PROFILER FACADE
class DataProfilerFacade:

    def __init__(self, table: pd.DataFrame):
        self.profiler = DataProfiler(table)

    def profile(self) -> None:    
        for column in self.profiler.table.columns:
            if pd.api.types.is_float_dtype(self.profiler.table[column]):
                self.profiler.profile_float_field(column)

            elif pd.api.types.is_string_dtype(self.profiler.table[column]):
                self.profiler.profile_string_field(column)