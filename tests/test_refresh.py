from .context import lux
import pytest
import pandas as pd
import numpy as np
from lux.utils import date_utils
from lux.executor.PandasExecutor import PandasExecutor
from lux.luxDataFrame.LuxDataframe import LuxDataFrame


def save_attr(ldf, attr):
	old_attr = getattr(ldf, attr)
	def check_consistent(new_ldf, changed_map):
		if attr in changed_map.keys():
			if changed_map[attr] == None:
				assert old_attr != getattr(new_ldf, attr), (attr)
			else:
				assert changed_map[attr] == getattr(new_ldf, attr), (attr)
		else:
			assert old_attr == getattr(new_ldf, attr), (attr)
	return check_consistent

def test_head_tail():
	ldf = pd.read_csv("lux/data/car.csv")
	check_functions = [save_attr(ldf, attr) for attr in lux.LuxDataFrame._metadata if hasattr(ldf, attr)]
	
	changed_map = {'dataTypeLookup': None, 'dataType': None, 'dataModelLookup': None, 'dataModel': None, 'uniqueValues': None, 'cardinality': None, \
						'xMinMax': None, 'yMinMax': None}

	new_ldf = ldf.head(5)
	assert new_ldf.dataTypeLookup['Horsepower'] == 'nominal'
	assert new_ldf.dataType['quantitative'] == ['MilesPerGal', 'Displacement', 'Acceleration']
	assert new_ldf.dataModelLookup['Horsepower'] == 'dimension'
	assert new_ldf.dataModel['measure'] == ['MilesPerGal', 'Displacement', 'Acceleration']
	assert len(new_ldf.uniqueValues['Cylinders']) > 0
	assert new_ldf.cardinality['Name'] == 5
	[f(new_ldf, changed_map) for f in check_functions]
	new_ldf = ldf.tail(5)
	[f(new_ldf, changed_map) for f in check_functions]

def test_rename():
	ldf = lux.LuxDataFrame(data={'a':[1,2,3,4,5],'b':[0,1,5,10,15]})
	changed_map = {'dataTypeLookup': None, 'dataType': None, 'dataModelLookup': None, 'dataModel': None, 'uniqueValues': None, 'cardinality': None, \
						'xMinMax': None, 'yMinMax': None}
	check_functions = [save_attr(ldf, attr) for attr in lux.LuxDataFrame._metadata if hasattr(ldf, attr)]
	new_ldf = ldf.rename(columns={'a':'new_a','b':'new_b'})
	[f(new_ldf, changed_map) for f in check_functions]

	#check inplace=True
	ldf = lux.LuxDataFrame(data={'a':[1,2,3,4,5],'b':[0,1,5,10,15]})
	changed_map = {'dataTypeLookup': None, 'dataType': None, 'dataModelLookup': None, 'dataModel': None, 'uniqueValues': None, 'cardinality': None, \
						'xMinMax': None, 'yMinMax': None}
	check_functions = [save_attr(ldf, attr) for attr in lux.LuxDataFrame._metadata if hasattr(ldf, attr)]
	ldf.rename(columns={'a':'new_a','b':'new_b'}, inplace=True)
	[f(ldf, changed_map) for f in check_functions]




