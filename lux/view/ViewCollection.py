from __future__ import annotations
from lux.vizLib.altair.AltairRenderer import AltairRenderer
from lux.utils.utils import check_import_lux_widget
from typing import List, Union, Callable, Dict
from lux.view.View import View
from lux.context.Spec import Spec
class ViewCollection():
	'''
	ViewCollection is a list of View objects. 
	'''
	def __init__(self,input_lst:Union[List[View],List[Spec]]):
		# Overloaded Constructor
		self.input_lst = input_lst
		if len(input_lst)>0:
			if (self._is_view_input()):
				self.collection = input_lst
				self.spec_lst = []
			else:
				self.spec_lst = input_lst
				self.collection = []
		else:
			self.collection = []
			self.spec_lst = []
	def get_exported(self) -> ViewCollection:
		"""
		Get selected views as exported View Collection

		Notes
        -----
		Convert the _exported_vis_idxs dictionary into a programmable ViewCollection
		Example _exported_vis_idxs : 
			{'View Collection': [0, 2]}
		
		Returns
		-------
		ViewCollection
		 	return a ViewCollection of selected views. -> ViewCollection(v1, v2...)
		"""        
		
		exported_vis_lst =self.widget._exportedVisIdxs
		if (exported_vis_lst=={}):
			import warnings
			warnings.warn("No visualization selected to export")
			return []
		else:
			exported_views = ViewCollection(list(map(self.__getitem__, exported_vis_lst["View Collection"])))
			return exported_views
	def remove_duplicates(self) -> None: 
		"""
		Removes duplicate views in View collection
		"""		
		self.collection = list(set(self.collection))
	def _is_view_input(self):
		if (type(self.input_lst[0])==View):
			return True
		elif (type(self.input_lst[0])==Spec):
			return False
	def __getitem__(self, key):
		return self.collection[key]
	def __setitem__(self, key, value):
		self.collection[key] = value
	def __len__(self):
		return len(self.collection)
	def __repr__(self):
		if len(self.collection) == 0:
			return str(self.input_lst)
		x_channel = ""
		y_channel = ""
		largest_mark = 0
		largest_filter = 0
		for view in self.collection: #finds longest x attribute among all views
			filter_spec = None
			for spec in view.spec_lst:
				if spec.value != "":
					filter_spec = spec

				if spec.aggregation != "":
					attribute = spec.aggregation.upper() + "(" + spec.attribute + ")"
				elif spec.bin_size > 0:
					attribute = "BIN(" + spec.attribute + ")"
				else:
					attribute = spec.attribute

				if spec.channel == "x" and len(x_channel) < len(attribute):
					x_channel = attribute
				if spec.channel == "y" and len(y_channel) < len(attribute):
					y_channel = attribute
			if len(view.mark) > largest_mark:
				largest_mark = len(view.mark)
			if filter_spec and len(str(filter_spec.value)) + len(filter_spec.attribute) > largest_filter:
				largest_filter = len(str(filter_spec.value)) + len(filter_spec.attribute) 
		views_repr = []
		largest_x_length = len(x_channel)
		largest_y_length = len(y_channel)
		for view in self.collection: #pads the shorter views with spaces before the y attribute
			filter_spec = None
			x_channel = ""
			y_channel = ""
			additional_channels = []
			for spec in view.spec_lst:
				if spec.value != "":
					filter_spec = spec

				if spec.aggregation != "":
					attribute = spec.aggregation.upper() + "(" + spec.attribute + ")"
				elif spec.bin_size > 0:
					attribute = "BIN(" + spec.attribute + ")"
				else:
					attribute = spec.attribute

				if spec.channel == "x":
					x_channel = attribute.ljust(largest_x_length)
				elif spec.channel == "y":
					y_channel = attribute
				elif spec.channel != "":
					additional_channels.append([spec.channel, attribute])
			if filter_spec:
				y_channel = y_channel.ljust(largest_y_length)
			elif largest_filter != 0:
				y_channel = y_channel.ljust(largest_y_length + largest_filter + 9)
			else:
				y_channel = y_channel.ljust(largest_y_length + largest_filter)
			if x_channel != "":
				x_channel = "x: " + x_channel + ", "
			if y_channel != "":
				y_channel = "y: " + y_channel
			aligned_mark = view.mark.ljust(largest_mark)
			str_additional_channels = ""
			for channel in additional_channels:
				str_additional_channels += ", " + channel[0] + ": " + channel[1]
			if filter_spec:
				aligned_filter = " -- [" + filter_spec.attribute + filter_spec.filter_op + str(filter_spec.value) + "]"
				aligned_filter = aligned_filter.ljust(largest_filter + 8)
				views_repr.append(f" <View  ({x_channel}{y_channel}{str_additional_channels} {aligned_filter}) mark: {aligned_mark}, score: {view.score:.2f} >") 
			else:
				views_repr.append(f" <View  ({x_channel}{y_channel}{str_additional_channels}) mark: {aligned_mark}, score: {view.score:.2f} >") 
		return '['+',\n'.join(views_repr)[1:]+']'
	def map(self,function):
		# generalized way of applying a function to each element
		return map(function, self.collection)
	
	def get(self,field_name):
		# Get the value of the field for all objects in the collection
		def get_field(d_obj):
			field_val = getattr(d_obj,field_name)
			# Might want to write catch error if key not in field
			return field_val
		return self.map(get_field)

	def set(self,field_name,field_val):
		return NotImplemented
	def set_plot_config(self,config_func:Callable):
		"""
		Modify plot aesthetic settings to the View Collection
		Currently only supported for Altair visualizations

		Parameters
		----------
		config_func : typing.Callable
			A function that takes in an AltairChart (https://altair-viz.github.io/user_guide/generated/toplevel/altair.Chart.html) as input and returns an AltairChart as output
		"""
		for view in self.collection:
			view.plot_config = config_func
	def clear_plot_config(self):
		for view in self.collection:
			view.plot_config = None
	def sort(self, remove_invalid=True, descending = True):
		# remove the items that have invalid (-1) score
		if (remove_invalid): self.collection = list(filter(lambda x: x.score!=-1,self.collection))
		# sort in-place by “score” by default if available, otherwise user-specified field to sort by
		self.collection.sort(key=lambda x: x.score, reverse=descending)

	def topK(self,k):
		#sort and truncate list to first K items
		self.sort(remove_invalid=True)
		return ViewCollection(self.collection[:k])
	def bottomK(self,k):
		#sort and truncate list to first K items
		self.sort(descending=False,remove_invalid=True)
		return ViewCollection(self.collection[:k])
	def normalize_score(self, invert_order = False):
		max_score = max(list(self.get("score")))
		for dobj in self.collection:
			dobj.score = dobj.score/max_score
			if (invert_order): dobj.score = 1 - dobj.score
	def _repr_html_(self):
		self.widget =  None
		from IPython.display import display
		from lux.luxDataFrame.LuxDataframe import LuxDataFrame
		# widget  = LuxDataFrame.render_widget(input_current_view=self,render_target="viewCollectionOnly")
		recommendation = {"action": "View Collection",
					  "description": "Shows a view collection defined by the context"}
		recommendation["collection"] = self

		check_import_lux_widget()
		import luxWidget
		recJSON = LuxDataFrame.rec_to_JSON([recommendation])
		self.widget =  luxWidget.LuxWidget(
				currentView={},
				recommendations=recJSON,
				context={}
			)
		display(self.widget)	
	
	def load(self, ldf) -> ViewCollection:
		"""
		Loading the data into the views in the ViewCollection by instantiating the specification and populating the view based on the data, effectively "materializing" the view.

		Parameters
		----------
		ldf : LuxDataframe
			Input Dataframe to be attached to the ViewCollection

		Returns
		-------
		ViewCollection
			Complete ViewCollection with fully-specified fields
		
		See Also
		--------
		lux.view.View.load
		"""		
		from lux.compiler.Parser import Parser
		from lux.compiler.Validator import Validator
		from lux.compiler.Compiler import Compiler
		from lux.executor.PandasExecutor import PandasExecutor #TODO: temporary (generalize to executor)
		if len(self.input_lst)>0:
			if (self._is_view_input()):
				for view in self.collection:
					view.spec_lst = Parser.parse(view.spec_lst)
					Validator.validate_spec(view.spec_lst,ldf)
				vc = Compiler.compile(ldf,ldf.context,self,enumerate_collection=False)
			else:
				self.spec_lst = Parser.parse(self.spec_lst)
				Validator.validate_spec(self.spec_lst,ldf)
				vc = Compiler.compile(ldf,self.spec_lst,self)
			PandasExecutor.execute(vc,ldf)
			return vc
		else:
			return self
