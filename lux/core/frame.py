import pandas as pd
import numpy as np
import sys
from lux.core.series import LuxSeries
from lux.vis.Clause import Clause
from lux.vis.Vis import Vis
from lux.vis.VisList import VisList
from lux.history.history import History
from lux.utils.utils import check_import_lux_widget, check_if_id_like
from lux.utils.date_utils import is_datetime_series
from lux.utils.message import Message
#import for benchmarking
import time
from typing import Optional, Dict, Union, List, Callable
import warnings
class LuxDataFrame(pd.DataFrame):
	'''
	A subclass of pd.DataFrame that supports all dataframe operations while housing other variables and functions for generating visual recommendations.
	'''
	# MUST register here for new properties!!
	_metadata = ['_intent','data_type_lookup','data_type',
				 'data_model_lookup','data_model','unique_values','cardinality','_rec_info', '_pandas_only',
				'_min_max','plot_config', '_current_vis','_widget', '_recommendation','_prev','_history']

	def __init__(self,*args, **kw):
		from lux.executor.PandasExecutor import PandasExecutor
		self._history = History()
		self._intent = []
		self._recommendation = {}
		self._current_vis = []
		self._prev = None
		super(LuxDataFrame, self).__init__(*args, **kw)
	
		self.executor_type = "Pandas"
		self.executor = PandasExecutor
		self.SQLconnection = ""
		self.table_name = ""

		self._default_pandas_display = True
		self._toggle_pandas_display = True
		self._plot_config = None
		self._message = Message()
		self._pandas_only=False
		# Metadata
		self.data_type_lookup = None
		self.data_type = None
		self.data_model_lookup = None
		self.data_model = None
		self.unique_values = None
		self.cardinality = None
		self._min_max = None
		self.pre_aggregated = None

	def _is_homogeneous_type(self) -> bool:
		#sys.stdout = open("test.txt", "w")
		print("_is_homogeneous_type,\n")
		#sys.stdout.close()
		return super(LuxDataFrame, self)._is_homogeneous_type()
	def _can_fast_transpose(self) -> bool:
		#sys.stdout = open("test.txt", "w")
		print("_can_fast_transpose,\n")
		#sys.stdout.close()
		return super(LuxDataFrame, self)._can_fast_transpose()
	def _repr_fits_vertical_(self) -> bool:
		#sys.stdout = open("test.txt", "w")
		print("_repr_fits_vertical_,\n")
		#sys.stdout.close()
		return super(LuxDataFrame, self)._repr_fits_vertical_()
	def _repr_fits_horizontal_(self) -> bool:
		#sys.stdout = open("test.txt", "w")
		print("_repr_fits_horizontal_,\n")
		#sys.stdout.close()
		return super(LuxDataFrame, self)._repr_fits_horizontal_()
	def _info_repr(self) -> bool:
		#sys.stdout = open("test.txt", "w")
		print("_info_repr,\n")
		#sys.stdout.close()
		return super(LuxDataFrame, self)._info_repr()
	def __len__(self) -> int:
		#sys.stdout = open("test.txt", "w")
		print("__len__,\n")
		#sys.stdout.close()
		return super(LuxDataFrame, self).__len__()
	def __matmul__(self, other):
		#sys.stdout = open("test.txt", "w")
		print("__matmul__,\n")
		#sys.stdout.close()
		return super(LuxDataFrame, self).__matmul__(other)
	def __rmatmul__(self, other):
		#sys.stdout = open("test.txt", "w")
		print("__rmatmul__,\n")
		#sys.stdout.close()
		return super(LuxDataFrame, self).__rmatmul__(other)
	def _from_arrays(cls, arrays, columns, index, dtype= None, verify_integrity = True):
		#sys.stdout = open("test.txt", "w")
		print("_from_arrays,\n")
		#sys.stdout.close()
		return super(LuxDataFrame, cls)._from_arrays(arrays, columns, index, dtype, verify_integrity)
	def _ixs(self, i: int, axis: int = 0):
		#sys.stdout = open("test.txt", "w")
		print("_ixs,\n")
		#sys.stdout.close()
		return super(LuxDataFrame, self)._ixs(i, axis)
	def _get_column_array(self, i: int):
		#sys.stdout = open("test.txt", "w")
		print("_get_column_array,\n")
		#sys.stdout.close()
		return super(LuxDataFrame, self)._ixs(i)
	def _iter_column_arrays(self):
		#sys.stdout = open("test.txt", "w")
		print("_iter_column_arrays,\n")
		#sys.stdout.close()
		return super(LuxDataFrame, self)._ixs()
	def _iter_column_arrays(self):
		#sys.stdout = open("test.txt", "w")
		print("_iter_column_arrays,\n")
		#sys.stdout.close()
		return super(LuxDataFrame, self)._ixs()
	def __getitem__(self, key):
		#sys.stdout = open("test.txt", "w")
		print("__getitem__,\n")
		#sys.stdout.close()
		return super(LuxDataFrame, self).__getitem__(key)
	def _getitem_bool_array(self, key):
		#sys.stdout = open("test.txt", "w")
		print("_getitem_bool_array,\n")
		#sys.stdout.close()
		return super(LuxDataFrame, self)._getitem_bool_array(key)
	def _getitem_multilevel(self, key):
		#sys.stdout = open("test.txt", "w")
		print("_getitem_multilevel,\n")
		#sys.stdout.close()
		return super(LuxDataFrame, self)._getitem_multilevel(key)
	def _get_value(self, index, col, takeable: bool = False):
		#sys.stdout = open("test.txt", "w")
		print("_get_value,\n")
		#sys.stdout.close()
		return super(LuxDataFrame, self)._get_value(index, col, takeable)
	def _get_value(self, index, col, takeable: bool = False):
		#sys.stdout = open("test.txt", "w")
		print("_get_value,\n")
		#sys.stdout.close()
		return super(LuxDataFrame, self)._get_value(index, col, takeable)
	def _setitem_slice(self, key, value):
		#sys.stdout = open("test.txt", "w")
		print("_setitem_slice,\n")
		#sys.stdout.close()
		return super(LuxDataFrame, self)._setitem_slice(key, value)
	def _setitem_array(self, key, value):
		#sys.stdout = open("test.txt", "w")
		print("_setitem_array,\n")
		#sys.stdout.close()
		return super(LuxDataFrame, self)._setitem_array(key, value)
	def _setitem_frame(self, key, value):
		#sys.stdout = open("test.txt", "w")
		print("_setitem_frame,\n")
		#sys.stdout.close()
		return super(LuxDataFrame, self)._setitem_frame(key, value)
	def _iset_item(self, loc, value):
		#sys.stdout = open("test.txt", "w")
		print("_iset_item,\n")
		#sys.stdout.close()
		return super(LuxDataFrame, self)._iset_item(loc, value)
	def _set_item(self, key, value):
		#sys.stdout = open("test.txt", "w")
		print("_set_item,\n")
		#sys.stdout.close()
		return super(LuxDataFrame, self)._set_item(key, value)
	def _set_value(self, index,  col, value, takeable):
		#sys.stdout = open("test.txt", "w")
		print("_set_value,\n")
		#sys.stdout.close()
		return super(LuxDataFrame, self)._set_value(index,  col, value, takeable)
	def _ensure_valid_index(self, value):
		#sys.stdout = open("test.txt", "w")
		print("_ensure_valid_index,\n")
		#sys.stdout.close()
		return super(LuxDataFrame, self)._ensure_valid_index(value)
	def _box_col_values(self, values, loc):
		#sys.stdout = open("test.txt", "w")
		print("_box_col_values,\n")
		#sys.stdout.close()
		return super(LuxDataFrame, self)._box_col_values(values, loc)
	def _sanitize_column(self, key, value, broadcast=True):
		#sys.stdout = open("test.txt", "w")
		print("_sanitize_column,\n")
		#sys.stdout.close()
		return super(LuxDataFrame, self)._sanitize_column(key, value, broadcast)
	def _series(self):
		#sys.stdout = open("test.txt", "w")
		print("_series,\n")
		#sys.stdout.close()
		return super(LuxDataFrame, self)._series()
	def _reindex_axes(self, axes, level, limit, tolerance, method, fill_value, copy):
		#sys.stdout = open("test.txt", "w")
		print("_reindex_axes,\n")
		#sys.stdout.close()
		return super(LuxDataFrame, self)._reindex_axes(axes, level, limit, tolerance, method, fill_value, copy)
	def _reindex_index(self, new_index, method, copy, level, fill_value=np.nan, limit=None, tolerance=None):
		#sys.stdout = open("test.txt", "w")
		print("_reindex_index,\n")
		#sys.stdout.close()
		return super(LuxDataFrame, self)._reindex_index(new_index, method, copy, level, fill_value, limit, tolerance)
	def _reindex_columns(self, new_columns, method, copy, level, fill_value=np.nan, limit=None, tolerance=None):
		#sys.stdout = open("test.txt", "w")
		print("_reindex_columns,\n")
		#sys.stdout.close()
		return super(LuxDataFrame, self)._reindex_columns(new_columns, method, copy, level, fill_value, limit, tolerance)
	def _reindex_multi(self, axes, copy, fill_value):
		#sys.stdout = open("test.txt", "w")
		print("_reindex_multi,\n")
		#sys.stdout.close()
		return super(LuxDataFrame, self)._reindex_multi(axes, copy, fill_value)
	def _replace_columnwise(self, mapping, inplace, regex):
		#sys.stdout = open("test.txt", "w")
		print("_replace_columnwise,\n")
		#sys.stdout.close()
		return super(LuxDataFrame, self)._replace_columnwise(mapping, inplace, regex)
	def _combine_frame(self, other, func, fill_value=None):
		#sys.stdout = open("test.txt", "w")
		print("_combine_frame,\n")
		#sys.stdout.close()
		return super(LuxDataFrame, self)._combine_frame(other, func, fill_value)
	def _construct_result(self, result):
		#sys.stdout = open("test.txt", "w")
		print("_construct_result,\n")
		#sys.stdout.close()
		return super(LuxDataFrame, self)._construct_result(result)
	def _gotitem(self, key, ndim, subset):
		#sys.stdout = open("test.txt", "w")
		print("_gotitem,\n")
		#sys.stdout.close()
		return super(LuxDataFrame, self)._gotitem(key, ndim, subset)
	def _aggregate(self, arg, axis, *args, **kwargs):
		#sys.stdout = open("test.txt", "w")
		print("_aggregate,\n")
		#sys.stdout.close()
		return super(LuxDataFrame, self)._aggregate(key, arg, axis, *args, **kwargs)
	def _join_compat(self, other, on=None, how="left", lsuffix="", rsuffix="", sort=False):
		#sys.stdout = open("test.txt", "w")
		print("_join_compat,\n")
		#sys.stdout.close()
		return super(LuxDataFrame, self)._join_compat(other, on, how, lsuffix, rsuffix, sort)
	def _count_level(self, level, axis=0, numeric_only=False):
		#sys.stdout = open("test.txt", "w")
		print("_count_level,\n")
		#sys.stdout.close()
		return super(LuxDataFrame, self)._count_level(level, axis, numeric_only)
	def _reduce(op, name, skipna, numeric_only, filter_ty, **kwds):
		#sys.stdout = open("test.txt", "w")
		print("_reduce,\n")
		#sys.stdout.close(op, name, skipna, numeric_only, filter_ty, **kwds)
		return super(LuxDataFrame, self)._reduce(level, axis, numeric_only)
	def _get_data():
		#sys.stdout = open("test.txt", "w")
		print("_get_data,\n")
		#sys.stdout.close()
		return super(LuxDataFrame, self)._get_data(level, axis, numeric_only)
	def _get_agg_axis(self, axis_num):
		#sys.stdout = open("test.txt", "w")
		print("_get_agg_axis,\n")
		#sys.stdout.close()
		return super(LuxDataFrame, self)._get_agg_axis(axis_num)





	@property
	def _constructor(self):
		#sys.stdout = open("test.txt", "w")
		print("_constructor,\n")
		#sys.stdout.close()
		return LuxDataFrame
	def __setitem__(self,key,value):
		#sys.stdout = open("test.txt", "w")
		print("__setitem__,\n")
		#sys.stdout.close()
		super(LuxDataFrame, self).__setitem__(key, value)
		self.expire_metadata()
		self.expire_recs()
	# @property
	# def _constructor_sliced(self):
	# 	def f(*args, **kwargs):
	# 		# adapted from https://github.com/pandas-dev/pandas/issues/13208#issuecomment-326556232
	# 		return LuxSeries(*args, **kwargs).__finalize__(self, method='inherit')
	# 	return f
	@property
	def history(self):
		return self._history
	def maintain_metadata(self):
		if (not hasattr(self,"_metadata_fresh") or not self._metadata_fresh ): # Check that metadata has not yet been computed
			if (len(self)>0): #only compute metadata information if the dataframe is non-empty
				self.compute_stats()
				self.compute_dataset_metadata()
				self._infer_structure()
				self._metadata_fresh = True
	def expire_recs(self):
		self._recs_fresh = False
		self.recommendation = None
		self.current_vis = None
		self._widget = None
		self._rec_info= None
	def expire_metadata(self):
		# Set metadata as null
		self._metadata_fresh = False
		self.data_type_lookup = None
		self.data_type = None
		self.data_model_lookup = None
		self.data_model = None
		self.unique_values = None
		self.cardinality = None
		self._min_max = None
		self.pre_aggregated = None

	#####################
	## Override Pandas ##
	#####################
	# def __finalize__(self,other, method: Optional[str] = None, **kwargs):
	#     print ("lux finalize")
	#     super(LuxDataFrame, self).__finalize__(other,method,**kwargs)
	#     self.expire_metadata()

	def _update_inplace(self,*args,**kwargs):
		super(LuxDataFrame, self)._update_inplace(*args,**kwargs)
		self.expire_metadata()
		self.expire_recs()
	@property
	def default_display(self):
		if (self._default_pandas_display):
			return "pandas"
		else:
			return "lux"
	@default_display.setter
	def default_display(self, type:str) -> None:
		"""
		Set the widget display to show Pandas by default or Lux by default
		Parameters
		----------
		type : str
			Default display type, can take either the string `lux` or `pandas` (regardless of capitalization)
		"""        
		if (type.lower()=="lux"):
			self._default_pandas_display = False
		elif (type.lower()=="pandas"):
			self._default_pandas_display = True
		else: 
			warnings.warn("Unsupported display type. Default display option should either be `lux` or `pandas`.",stacklevel=2)
	def _infer_structure(self):
		# If the dataframe is very small and the index column is not a range index, then it is likely that this is an aggregated data
		is_multi_index_flag = self.index.nlevels !=1
		not_int_index_flag = self.index.dtype !='int64'
		small_df_flag = len(self)<100
		self.pre_aggregated = (is_multi_index_flag or not_int_index_flag) and small_df_flag 
		if ("Number of Records" in self.columns):
			self.pre_aggregated = True
		very_small_df_flag =  len(self)<=10
		if (very_small_df_flag):
			self.pre_aggregated = True
	def set_executor_type(self, exe):
		if (exe =="SQL"):
			import pkgutil
			if (pkgutil.find_loader("psycopg2") is None):
				raise ImportError("psycopg2 is not installed. Run `pip install psycopg2' to install psycopg2 to enable the Postgres connection.")
			else:
				import psycopg2
			from lux.executor.SQLExecutor import SQLExecutor
			self.executor = SQLExecutor
		else:
			from lux.executor.PandasExecutor import PandasExecutor
			self.executor = PandasExecutor
		self.executor_type = exe
	@property 
	def plot_config(self):
		return self._plot_config
	@plot_config.setter
	def plot_config(self,config_func:Callable):
		"""
		Modify plot aesthetic settings to all visualizations in the dataframe display
		Currently only supported for Altair visualizations
		Parameters
		----------
		config_func : Callable
			A function that takes in an AltairChart (https://altair-viz.github.io/user_guide/generated/toplevel/altair.Chart.html) as input and returns an AltairChart as output
		
		Example
		----------
		Changing the color of marks and adding a title for all charts displayed for this dataframe
		>>> df = pd.read_csv("lux/data/car.csv")
		>>> def changeColorAddTitle(chart):
				chart = chart.configure_mark(color="red") # change mark color to red
				chart.title = "Custom Title" # add title to chart
				return chart
		>>> df.plot_config = changeColorAddTitle
		>>> df
		Change the opacity of all scatterplots displayed for this dataframe
		>>> df = pd.read_csv("lux/data/olympic.csv")
		>>> def changeOpacityScatterOnly(chart):
				if chart.mark=='circle':
					chart = chart.configure_mark(opacity=0.1) # lower opacity
				return chart
		>>> df.plot_config = changeOpacityScatterOnly
		>>> df
		"""        
		self._plot_config = config_func
		self._recs_fresh=False
	def clear_plot_config(self):
		self._plot_config = None
		self._recs_fresh=False
	
	@property
	def intent(self):
		return self._intent
	@intent.setter
	def intent(self, intent_input:Union[List[Union[str, Clause]],Vis]):
		is_list_input = isinstance(intent_input,list)
		is_vis_input = isinstance(intent_input,Vis)
		if not (is_list_input or is_vis_input):
			raise TypeError("Input intent must be either a list (of strings or lux.Clause) or a lux.Vis object."
					"\nSee more at: https://lux-api.readthedocs.io/en/latest/source/guide/intent.html"
					)
		if is_list_input:
			self.set_intent(intent_input)
		elif is_vis_input:
			self.set_intent_as_vis(intent_input)
	def clear_intent(self):
		self.intent = []
	def set_intent(self, intent:List[Union[str, Clause]]):
		"""
		Main function to set the intent of the dataframe.
		The intent input goes through the parser, so that the string inputs are parsed into a lux.Clause object.

		Parameters
		----------
		intent : List[str,Clause]
			intent list, can be a mix of string shorthand or a lux.Clause object

		Notes
		-----
			:doc:`../guide/clause`
		"""        
		self.expire_recs()
		self._intent = intent
		self._parse_validate_compile_intent()
	def _parse_validate_compile_intent(self):
		from lux.processor.Parser import Parser
		from lux.processor.Validator import Validator
		self._intent = Parser.parse(self._intent)
		Validator.validate_intent(self._intent,self)
		self.maintain_metadata()
		from lux.processor.Compiler import Compiler
		self.current_vis = Compiler.compile_intent(self, self._intent)
		
	def copy_intent(self):
		#creates a true copy of the dataframe's intent
		output = []
		for clause in self._intent:
			temp_clause = clause.copy_clause()
			output.append(temp_clause)
		return(output)

	def set_intent_as_vis(self,vis:Vis):
		"""
		Set intent of the dataframe as the Vis

		Parameters
		----------
		vis : Vis
		"""        
		self.expire_recs()
		self._intent = vis._inferred_intent
		self._parse_validate_compile_intent()

	def to_pandas(self):
		import lux.core
		return lux.core.originalDF(self,copy=False)
	
	@property
	def recommendation(self):
		return self._recommendation
	@recommendation.setter
	def recommendation(self,recommendation:Dict):
		self._recommendation = recommendation
	@property
	def current_vis(self):
		return self._current_vis
	@current_vis.setter
	def current_vis(self,current_vis:Dict):
		self._current_vis = current_vis
	def __repr__(self):
		# TODO: _repr_ gets called from _repr_html, need to get rid of this call
		#sys.stdout = open("test.txt", "w")
		print("__repr__,\n")
		#sys.stdout.close()
		return ""
	#######################################################
	############ Metadata: data type, model #############
	#######################################################
	def compute_dataset_metadata(self):
		self.data_type_lookup = {}
		self.data_type = {}
		self.compute_data_type()
		self.data_model_lookup = {}
		self.data_model = {}
		self.compute_data_model()

	def compute_data_type(self):
		for attr in list(self.columns):
			if (isinstance(attr,pd._libs.tslibs.timestamps.Timestamp)): 
				# If timestamp, make the dictionary keys the _repr_ (e.g., TimeStamp('2020-04-05 00.000')--> '2020-04-05')
				self.data_type_lookup[attr] = "temporal"
			elif str(attr).lower() in ["month", "year","day","date","time"]:
				self.data_type_lookup[attr] = "temporal"
			elif self.dtypes[attr] == "float64":
				self.data_type_lookup[attr] = "quantitative"
			elif self.dtypes[attr] == "int64":
				# See if integer value is quantitative or nominal by checking if the ratio of cardinality/data size is less than 0.4 and if there are less than 10 unique values
				if (self.pre_aggregated):
					if (self.cardinality[attr]==len(self)):
						self.data_type_lookup[attr] = "nominal"
				if self.cardinality[attr]/len(self) < 0.4 and self.cardinality[attr]<10: 
					self.data_type_lookup[attr] = "nominal"
				elif check_if_id_like(self,attr): 
					self.data_type_lookup[attr] = "id"
				else:
					self.data_type_lookup[attr] = "quantitative"
			# Eliminate this clause because a single NaN value can cause the dtype to be object
			elif self.dtypes[attr] == "object":
				self.data_type_lookup[attr] = "nominal"
			elif is_datetime_series(self.dtypes[attr]): #check if attribute is any type of datetime dtype
				self.data_type_lookup[attr] = "temporal"
		# for attr in list(df.dtypes[df.dtypes=="int64"].keys()):
		# 	if self.cardinality[attr]>50:
		if (self.index.dtype !='int64' and self.index.name):
			self.data_type_lookup[self.index.name] = "nominal"
		self.data_type = self.mapping(self.data_type_lookup)

		from pandas.api.types import is_datetime64_any_dtype as is_datetime
		non_datetime_attrs = []
		for attr in self.columns:
			if self.data_type_lookup[attr] == 'temporal' and not is_datetime(self[attr]):
				non_datetime_attrs.append(attr)
		if len(non_datetime_attrs) == 1:
			warnings.warn(
		            f"\nLux detects that the attribute '{non_datetime_attrs[0]}' may be temporal.\n" 
		            "In order to display visualizations for this attribute accurately, temporal attributes should be converted to Pandas Datetime objects.\n\n"
		            "Please consider converting this attribute using the pd.to_datetime function and providing a 'format' parameter to specify datetime format of the attribute.\n"
		            "For example, you can convert the 'month' attribute in a dataset to Datetime type via the following command:\n\n\t df['month'] = pd.to_datetime(df['month'], format='%m')\n\n"
		            "See more at: https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.to_datetime.html\n"
		        	,stacklevel=2)
		elif len(non_datetime_attrs) > 1:
			warnings.warn(
		            f"\nLux detects that attributes {non_datetime_attrs} may be temporal.\n" 
		            "In order to display visualizations for these attributes accurately, temporal attributes should be converted to Pandas Datetime objects.\n\n"
		            "Please consider converting these attributes using the pd.to_datetime function and providing a 'format' parameter to specify datetime format of the attribute.\n"
		            "For example, you can convert the 'month' attribute in a dataset to Datetime type via the following command:\n\n\t df['month'] = pd.to_datetime(df['month'], format='%m')\n\n"
		            "See more at: https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.to_datetime.html\n"
		        	,stacklevel=2)
	def compute_data_model(self):
		self.data_model = {
			"measure": self.data_type["quantitative"],
			"dimension": self.data_type["ordinal"] + self.data_type["nominal"] + self.data_type["temporal"]
		}
		self.data_model_lookup = self.reverseMapping(self.data_model)

	def mapping(self, rmap):
		group_map = {}
		for val in ["quantitative","id", "ordinal", "nominal", "temporal"]:
			group_map[val] = list(filter(lambda x: rmap[x] == val, rmap))
		return group_map


	def reverseMapping(self, map):
		reverse_map = {}
		for valKey in map:
			for val in map[valKey]:
				reverse_map[val] = valKey
		return reverse_map

	def compute_stats(self):
		# precompute statistics
		self.unique_values = {}
		self._min_max = {}
		self.cardinality = {}

		for attribute in self.columns:
			
			if (isinstance(attribute,pd._libs.tslibs.timestamps.Timestamp)): 
				# If timestamp, make the dictionary keys the _repr_ (e.g., TimeStamp('2020-04-05 00.000')--> '2020-04-05')
				attribute_repr = str(attribute._date_repr)
			else:
				attribute_repr = attribute
			if self.dtypes[attribute] != "float64":# and not pd.api.types.is_datetime64_ns_dtype(self.dtypes[attribute]):
				self.unique_values[attribute_repr] = list(self[attribute].unique())
				self.cardinality[attribute_repr] = len(self.unique_values[attribute])
			else:   
				self.cardinality[attribute_repr] = 999 # special value for non-numeric attribute
			if self.dtypes[attribute] == "float64" or self.dtypes[attribute] == "int64":
				self._min_max[attribute_repr] = (self[attribute].min(), self[attribute].max())
		if (self.index.dtype !='int64'):
			index_column_name = self.index.name
			self.unique_values[index_column_name] = list(self.index)
			self.cardinality[index_column_name] = len(self.index)
	#######################################################
	########## SQL Metadata, type, model schema ###########
	#######################################################

	def set_SQL_connection(self, connection, t_name):
		self.SQLconnection = connection
		self.table_name = t_name
		self.compute_SQL_dataset_metadata()
		self.set_executor_type("SQL")

	def compute_SQL_dataset_metadata(self):
		self.get_SQL_attributes()
		for attr in list(self.columns):
			self[attr] = None
		self.data_type_lookup = {}
		self.data_type = {}
		#####NOTE: since we aren't expecting users to do much data processing with the SQL database, should we just keep this 
		#####      in the initialization and do it just once
		self.compute_SQL_data_type()
		self.compute_SQL_stats()
		self.data_model_lookup = {}
		self.data_model = {}
		self.compute_data_model()

	def compute_SQL_stats(self):
		# precompute statistics
		self.unique_values = {}
		self._min_max = {}

		self.get_SQL_unique_values()
		#self.get_SQL_cardinality()
		for attribute in self.columns:
			if self.data_type_lookup[attribute] == 'quantitative':
				self._min_max[attribute] = (self[attribute].min(), self[attribute].max())

	def get_SQL_attributes(self):
		if "." in self.table_name:
			table_name = self.table_name[self.table_name.index(".")+1:]
		else:
			table_name = self.table_name
		attr_query = "SELECT column_name FROM INFORMATION_SCHEMA.COLUMNS where TABLE_NAME = '{}'".format(table_name)
		attributes = list(pd.read_sql(attr_query, self.SQLconnection)['column_name'])
		for attr in attributes:
			self[attr] = None

	def get_SQL_cardinality(self):
		cardinality = {}
		for attr in list(self.columns):
			card_query = pd.read_sql("SELECT Count(Distinct({})) FROM {}".format(attr, self.table_name), self.SQLconnection)
			cardinality[attr] = list(card_query["count"])[0]
		self.cardinality = cardinality

	def get_SQL_unique_values(self):
		unique_vals = {}
		for attr in list(self.columns):
			unique_query = pd.read_sql("SELECT Distinct({}) FROM {}".format(attr, self.table_name), self.SQLconnection)
			unique_vals[attr] = list(unique_query[attr])
		self.unique_values = unique_vals

	def compute_SQL_data_type(self):
		data_type_lookup = {}
		sql_dtypes = {}
		self.get_SQL_cardinality()
		if "." in self.table_name:
			table_name = self.table_name[self.table_name.index(".")+1:]
		else:
			table_name = self.table_name
		#get the data types of the attributes in the SQL table
		for attr in list(self.columns):
			datatype_query = "SELECT DATA_TYPE FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '{}' AND COLUMN_NAME = '{}'".format(table_name, attr)
			datatype = list(pd.read_sql(datatype_query, self.SQLconnection)['data_type'])[0]
			sql_dtypes[attr] = datatype

		data_type = {"quantitative":[], "ordinal":[], "nominal":[], "temporal":[]}
		for attr in list(self.columns):
			if str(attr).lower() in ["month", "year"]:
				data_type_lookup[attr] = "temporal"
				data_type["temporal"].append(attr)
			elif sql_dtypes[attr] in ["character", "character varying", "boolean", "uuid", "text"]:
				data_type_lookup[attr] = "nominal"
				data_type["nominal"].append(attr)
			elif sql_dtypes[attr] in ["integer", "real", "smallint", "smallserial", "serial"]:
				if self.cardinality[attr] < 13:
					data_type_lookup[attr] = "nominal"
					data_type["nominal"].append(attr)
				else:
					data_type_lookup[attr] = "quantitative"
					data_type["quantitative"].append(attr)
			elif "time" in sql_dtypes[attr] or "date" in sql_dtypes[attr]:
				data_type_lookup[attr] = "temporal"
				data_type["temporal"].append(attr)
		self.data_type_lookup = data_type_lookup
		self.data_type = data_type
	def _append_rec(self,rec_infolist,recommendations:Dict):
		if (recommendations["collection"] is not None and len(recommendations["collection"])>0):
			rec_infolist.append(recommendations)
	def maintain_recs(self):
		# `rec_df` is the dataframe to generate the recommendations on
		show_prev = False # flag indicating whether rec_df is showing previous df or current self
		if self._prev is not None:
			rec_df = self._prev
			rec_df._message = Message()	
			rec_df.maintain_metadata() # the prev dataframe may not have been printed before
			last_event = self.history._events[-1].name
			rec_df._message.append(f"Lux is visualizing the previous version of the dataframe before you applied <code>{last_event}</code>.")
			show_prev = True
		else:
			rec_df = self
			rec_df._message = Message()	
		# Add warning message if there exist ID fields
		for id_field in rec_df.data_type["id"]:
			rec_df._message.append(f"<code>{id_field}</code> is not visualized since it resembles an ID field.")
		rec_df._prev = None # reset _prev
		
		if (not hasattr(rec_df,"_recs_fresh") or not rec_df._recs_fresh ): # Check that recs has not yet been computed
			rec_infolist = []
			from lux.action.custom import custom
			from lux.action.correlation import correlation
			from lux.action.univariate import univariate
			from lux.action.enhance import enhance
			from lux.action.filter import filter
			from lux.action.generalize import generalize
			from lux.action.row_group import row_group
			from lux.action.column_group import column_group

			if (rec_df.pre_aggregated):
				if (rec_df.columns.name is not None):
					rec_df._append_rec(rec_infolist, row_group(rec_df))
				if (rec_df.index.name is not None):
					rec_df._append_rec(rec_infolist, column_group(rec_df))
			else:
				if (rec_df.current_vis is None):
					no_vis = True
					one_current_vis = False
					multiple_current_vis = False
				else:
					no_vis = len(rec_df.current_vis) == 0
					one_current_vis = len(rec_df.current_vis) == 1
					multiple_current_vis = len(rec_df.current_vis) > 1

				if (no_vis):
					rec_df._append_rec(rec_infolist, correlation(rec_df))
					rec_df._append_rec(rec_infolist, univariate(rec_df,"quantitative"))
					rec_df._append_rec(rec_infolist, univariate(rec_df,"nominal"))
					rec_df._append_rec(rec_infolist, univariate(rec_df,"temporal"))
				elif (one_current_vis):
					rec_df._append_rec(rec_infolist, enhance(rec_df))
					rec_df._append_rec(rec_infolist, filter(rec_df))
					rec_df._append_rec(rec_infolist, generalize(rec_df))
				elif (multiple_current_vis):
					rec_df._append_rec(rec_infolist, custom(rec_df))
				
			# Store _rec_info into a more user-friendly dictionary form
			rec_df.recommendation = {}
			for rec_info in rec_infolist: 
				action_type = rec_info["action"]
				vlist = rec_info["collection"]
				if (rec_df._plot_config):
					for vis in rec_df.current_vis: vis._plot_config = rec_df.plot_config
					for vis in vlist: vis._plot_config = rec_df.plot_config
				if (len(vlist)>0):
					rec_df.recommendation[action_type]  = vlist
			rec_df._rec_info = rec_infolist
			self._widget = rec_df.render_widget()
		elif (show_prev): # re-render widget for the current dataframe if previous rec is not recomputed
			self._widget = rec_df.render_widget()
		self._recs_fresh = True


	#######################################################
	############## LuxWidget Result Display ###############
	#######################################################
	@property
	def widget(self):
		if(self._widget):
			return self._widget
	@property
	def exported(self) -> Union[Dict[str,VisList], VisList]:
		"""
		Get selected visualizations as exported Vis List

		Notes
		-----
		Convert the _exportedVisIdxs dictionary into a programmable VisList
		Example _exportedVisIdxs : 
			{'Correlation': [0, 2], 'Occurrence': [1]}
		indicating the 0th and 2nd vis from the `Correlation` tab is selected, and the 1st vis from the `Occurrence` tab is selected.
		
		Returns
		-------
		Union[Dict[str,VisList], VisList]
			When there are no exported vis, return empty list -> []
			When all the exported vis is from the same tab, return a VisList of selected visualizations. -> VisList(v1, v2...)
			When the exported vis is from the different tabs, return a dictionary with the action name as key and selected visualizations in the VisList. -> {"Enhance": VisList(v1, v2...), "Filter": VisList(v5, v7...), ..}
		"""
		if not hasattr(self,"_widget"):
			warnings.warn(
						"\nNo widget attached to the dataframe."
						"Please assign dataframe to an output variable.\n"
						"See more: https://lux-api.readthedocs.io/en/latest/source/guide/FAQ.html#troubleshooting-tips"
						, stacklevel=2)
			return []
		exported_vis_lst =self._widget._exportedVisIdxs
		exported_vis = [] 
		if (exported_vis_lst=={}):
			warnings.warn(
				"\nNo visualization selected to export.\n"
				"See more: https://lux-api.readthedocs.io/en/latest/source/guide/FAQ.html#troubleshooting-tips"
				,stacklevel=2)
			return []
		if len(exported_vis_lst) == 1 and "currentVis" in exported_vis_lst:
			return self.current_vis
		elif len(exported_vis_lst) > 1: 
			exported_vis  = {}
			if ("currentVis" in exported_vis_lst):
				exported_vis["Current Vis"] = self.current_vis
			for export_action in exported_vis_lst:
				if (export_action != "currentVis"):
					exported_vis[export_action] = VisList(list(map(self.recommendation[export_action].__getitem__, exported_vis_lst[export_action])))
			return exported_vis
		elif len(exported_vis_lst) == 1 and ("currentVis" not in exported_vis_lst): 
			export_action = list(exported_vis_lst.keys())[0]
			exported_vis = VisList(list(map(self.recommendation[export_action].__getitem__, exported_vis_lst[export_action])))
			return exported_vis
		else:
			warnings.warn(
				"\nNo visualization selected to export.\n"
				"See more: https://lux-api.readthedocs.io/en/latest/source/guide/FAQ.html#troubleshooting-tips"
				,stacklevel=2)
			return []

	def _repr_html_(self):
		#sys.stdout = open("test.txt", "w")
		print("_repr_html_,\n")
		#sys.stdout.close()
		from IPython.display import display
		from IPython.display import clear_output
		import ipywidgets as widgets
		
		try: 
			if (self._pandas_only):
				display(self.display_pandas())
				self._pandas_only=False
			else:
				if(self.index.nlevels>=2 or self.columns.nlevels >= 2):
					warnings.warn(
									"\nLux does not currently support dataframes "
									"with hierarchical indexes.\n"
									"Please convert the dataframe into a flat "
									"table via `pandas.DataFrame.reset_index`.\n",
									stacklevel=2,
								)
					display(self.display_pandas())
					return

				if (len(self)<=0):
					warnings.warn("\nLux can not operate on an empty dataframe.\nPlease check your input again.\n",stacklevel=2)
					display(self.display_pandas()) 
					return
				if (len(self.columns)<=1):
					warnings.warn("\nLux defaults to Pandas when there is only a single column.",stacklevel=2)
					display(self.display_pandas()) 
					return
				self.maintain_metadata()
				
				if (self._intent!=[] and (not hasattr(self,"_compiled") or not self._compiled)):
					from lux.processor.Compiler import Compiler
					self.current_vis = Compiler.compile_intent(self, self._intent)

				self._toggle_pandas_display = self._default_pandas_display # Reset to Pandas Vis everytime            
				
				# df_to_display.maintain_recs() # compute the recommendations (TODO: This can be rendered in another thread in the background to populate self._widget)
				self.maintain_recs()
			
				# box = widgets.Box(layout=widgets.Layout(display='inline'))
				button = widgets.Button(description="Toggle Pandas/Lux",layout=widgets.Layout(width='140px',top='5px'))
				output = widgets.Output()
				# box.children = [button,output]
				# output.children = [button]
				# display(box)
				display(button,output)
				def on_button_clicked(b):
					with output:
						if (b):
							self._toggle_pandas_display = not self._toggle_pandas_display
						clear_output()
						if (self._toggle_pandas_display):
							display(self.display_pandas())
						else:
							# b.layout.display = "none"
							display(self._widget)
							# b.layout.display = "inline-block"
				button.on_click(on_button_clicked)
				on_button_clicked(None)
		except(KeyboardInterrupt,SystemExit):
			raise
		except:
			warnings.warn(
					"\nUnexpected error in rendering Lux widget and recommendations. "
					"Falling back to Pandas display.\n\n" 
					"Please report this issue on Github: https://github.com/lux-org/lux/issues "
				,stacklevel=2)
			display(self.display_pandas())
	def display_pandas(self):
		return self.to_pandas()
	def render_widget(self, renderer:str ="altair", input_current_vis=""):
		"""
		Generate a LuxWidget based on the LuxDataFrame
		
		Structure of widgetJSON: 
		{
			'current_vis': {}, 
			'recommendation': [
				{
					'action': 'Correlation', 
					'description': "some description",
					'vspec': [
						{Vega-Lite spec for vis 1},
						{Vega-Lite spec for vis 2},
						...
					]
				},
				... repeat for other actions
			]
		}
		Parameters
		----------
		renderer : str, optional
			Choice of visualization rendering library, by default "altair"
		input_current_vis : lux.LuxDataFrame, optional
			User-specified current vis to override default Current Vis, by default 
		"""       
		check_import_lux_widget()
		import luxWidget
		widgetJSON = self.to_JSON(self._rec_info, input_current_vis=input_current_vis)
		return luxWidget.LuxWidget(
			currentVis=widgetJSON["current_vis"],
			recommendations=widgetJSON["recommendation"],
			intent=LuxDataFrame.intent_to_string(self._intent),
			message = self._message.to_html()
		)
	@staticmethod
	def intent_to_JSON(intent):
		from lux.utils import utils

		filter_specs = utils.get_filter_specs(intent)
		attrs_specs = utils.get_attrs_specs(intent)
		
		intent = {}
		intent['attributes'] = [clause.attribute for clause in attrs_specs]
		intent['filters'] = [clause.attribute for clause in filter_specs]
		return intent
	@staticmethod
	def intent_to_string(intent):
		if (intent):
			return ", ".join([clause.to_string() for clause in intent])
		else:
			return ""

	def to_JSON(self, rec_infolist, input_current_vis=""):
		widget_spec = {}
		if (self.current_vis): 
			self.executor.execute(self.current_vis, self)
			widget_spec["current_vis"] = LuxDataFrame.current_vis_to_JSON(self.current_vis, input_current_vis)
		else:
			widget_spec["current_vis"] = {}
		widget_spec["recommendation"] = []
		
		# Recommended Collection
		recCollection = LuxDataFrame.rec_to_JSON(rec_infolist)
		widget_spec["recommendation"].extend(recCollection)
		return widget_spec
	
	@staticmethod
	def current_vis_to_JSON(vlist, input_current_vis=""):
		current_vis_spec = {}
		numVC = len(vlist) #number of visualizations in the vis list
		if (numVC==1):
			current_vis_spec = vlist[0].render_VSpec()
		elif (numVC>1):
			pass
		return current_vis_spec
	@staticmethod
	def rec_to_JSON(recs):
		rec_lst = []
		import copy
		rec_copy = copy.deepcopy(recs)
		for idx,rec in enumerate(rec_copy):
			if (len(rec["collection"])>0):
				rec["vspec"] = []
				for vis in rec["collection"]:
					chart = vis.render_VSpec()
					rec["vspec"].append(chart)
				rec_lst.append(rec)
				# delete DataObjectCollection since not JSON serializable
				del rec_lst[idx]["collection"]
		return rec_lst
	
	# Overridden Pandas Functions
	def head(self, n: int = 5):
		self._prev = self
		self._history.append_event("head", n=5)
		return super(LuxDataFrame, self).head(n)
	
	def tail(self, n: int = 5):
		self._prev = self
		self._history.append_event("tail", n=5)
		return super(LuxDataFrame, self).tail(n)
	
	def info(self, *args, **kwargs):
		self._pandas_only=True
		self._history.append_event("info",*args, **kwargs)
		return super(LuxDataFrame, self).info(*args, **kwargs)

	def describe(self, *args, **kwargs):
		self._pandas_only=True
		self._history.append_event("describe",*args, **kwargs)
		return super(LuxDataFrame, self).describe(*args, **kwargs)
