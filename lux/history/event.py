#  Copyright 2019-2020 The Lux Authors.
# 
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

class Event():
	"""
	Event represents a single operation applied to the dataframe, with input arguments of operation recorded
	"""
	def __init__(self,name,*args,**kwargs):
		self.name = name
		self.args = args
		self.kwargs = kwargs
	def __repr__(self):
		if (self.args==() and self.kwargs=={}):
			return f"<Event: {self.name}>"
		else:
			return f"<Event: {self.name} -- args={self.args}, kwargs={self.kwargs}>"