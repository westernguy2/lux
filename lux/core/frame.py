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

import pandas as pd
from lux.core.series import LuxSeries
from lux.vis.Clause import Clause
from lux.vis.Vis import Vis
from lux.vis.VisList import VisList
from lux.history.history import History
from lux.utils.message import Message
from lux.utils.utils import check_import_lux_widget
from typing import Dict, Union, List, Callable
import warnings
import lux


class LuxDataFrame(pd.DataFrame):
    """
    A subclass of pd.DataFrame that supports all dataframe operations while housing other variables and functions for generating visual recommendations.
    """

    # MUST register here for new properties!!
    _metadata = [
        "_intent",
        "data_type_lookup",
        "data_type",
        "data_model_lookup",
        "data_model",
        "unique_values",
        "cardinality",
        "_rec_info",
        "_pandas_only",
        "_min_max",
        "plot_config",
        "_current_vis",
        "_widget",
        "_recommendation",
        "_prev",
        "_history",
        "_saved_export",
    ]

    recent_record = None

    def __init__(self, *args, **kw):
        from lux.executor.PandasExecutor import PandasExecutor

        self._history = History()
        self._intent = []
        self._recommendation = {}
        self._saved_export = None
        self._current_vis = []
        self._prev = None
        super(LuxDataFrame, self).__init__(*args, **kw)

        self.executor_type = "Pandas"
        self.executor = PandasExecutor()
        self.SQLconnection = ""
        self.table_name = ""

        self._sampled = None
        self._default_pandas_display = True
        self._toggle_pandas_display = True
        self._plot_config = None
        self._message = Message()
        self._pandas_only = False
        # Metadata
        self.data_type_lookup = None
        self.data_type = None
        self.data_model_lookup = None
        self.data_model = None
        self.unique_values = None
        self.cardinality = None
        self._min_max = None
        self.pre_aggregated = None
        warnings.formatwarning = lux.warning_format

    @property
    def _constructor(self):
        return LuxDataFrame

    @property
    def _constructor_sliced(self):
        def f(*args, **kwargs):
            s = LuxSeries(*args, **kwargs)
            for attr in self._metadata:  # propagate metadata
                s.__dict__[attr] = getattr(self, attr, None)
            return s

        return f

    @property
    def history(self):
        return self._history

    def maintain_metadata(self):
        # Check that metadata has not yet been computed
        if not hasattr(self, "_metadata_fresh") or not self._metadata_fresh:
            # only compute metadata information if the dataframe is non-empty
            if len(self) > 0:
                self.executor.compute_stats(self)
                self.executor.compute_dataset_metadata(self)
                self._infer_structure()
                self._metadata_fresh = True

    def expire_recs(self):
        self._recs_fresh = False
        self.recommendation = {}
        self.current_vis = None
        self._widget = None
        self._rec_info = None
        self._sampled = None

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
    def __getattr__(self, name):
        ret_value = super(LuxDataFrame, self).__getattr__(name)
        self.expire_metadata()
        self.expire_recs()
        return ret_value

    def _set_axis(self, axis, labels):
        super(LuxDataFrame, self)._set_axis(axis, labels)
        self.expire_metadata()
        self.expire_recs()

    def _update_inplace(self, *args, **kwargs):
        super(LuxDataFrame, self)._update_inplace(*args, **kwargs)
        self.expire_metadata()
        self.expire_recs()

    def _set_item(self, key, value):
        super(LuxDataFrame, self)._set_item(key, value)
        self.expire_metadata()
        self.expire_recs()

    def _infer_structure(self):
        # If the dataframe is very small and the index column is not a range index, then it is likely that this is an aggregated data
        is_multi_index_flag = self.index.nlevels != 1
        not_int_index_flag = self.index.dtype != "int64"
        small_df_flag = len(self) < 100
        self.pre_aggregated = (is_multi_index_flag or not_int_index_flag) and small_df_flag
        if "Number of Records" in self.columns:
            self.pre_aggregated = True
        very_small_df_flag = len(self) <= 10
        if very_small_df_flag:
            self.pre_aggregated = True

    def set_executor_type(self, exe):
        if exe == "SQL":
            import pkgutil

            if pkgutil.find_loader("psycopg2") is None:
                raise ImportError(
                    "psycopg2 is not installed. Run `pip install psycopg2' to install psycopg2 to enable the Postgres connection."
                )
            else:
                import psycopg2
            from lux.executor.SQLExecutor import SQLExecutor

            self.executor = SQLExecutor
        else:
            from lux.executor.PandasExecutor import PandasExecutor

            self.executor = PandasExecutor()
        self.executor_type = exe

    @property
    def plot_config(self):
        return self._plot_config

    @plot_config.setter
    def plot_config(self, config_func: Callable):
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
        self._recs_fresh = False

    def clear_plot_config(self):
        self._plot_config = None
        self._recs_fresh = False

    @property
    def intent(self):
        return self._intent

    @intent.setter
    def intent(self, intent_input: Union[List[Union[str, Clause]], Vis]):
        is_list_input = isinstance(intent_input, list)
        is_vis_input = isinstance(intent_input, Vis)
        if not (is_list_input or is_vis_input):
            raise TypeError(
                "Input intent must be either a list (of strings or lux.Clause) or a lux.Vis object."
                "\nSee more at: https://lux-api.readthedocs.io/en/latest/source/guide/intent.html"
            )
        if is_list_input:
            self.set_intent(intent_input)
        elif is_vis_input:
            self.set_intent_as_vis(intent_input)

    def clear_intent(self):
        self.intent = []
        self.expire_recs()

    def set_intent(self, intent: List[Union[str, Clause]]):
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
        self.maintain_metadata()
        from lux.processor.Parser import Parser
        from lux.processor.Validator import Validator

        self._intent = Parser.parse(self._intent)
        Validator.validate_intent(self._intent, self)
        self.maintain_metadata()
        from lux.processor.Compiler import Compiler

        self.current_vis = Compiler.compile_intent(self, self._intent)

    def copy_intent(self):
        # creates a true copy of the dataframe's intent
        output = []
        for clause in self._intent:
            temp_clause = clause.copy_clause()
            output.append(temp_clause)
        return output

    def set_intent_as_vis(self, vis: Vis):
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

        return lux.core.originalDF(self, copy=False)

    @property
    def recommendation(self):
        return self._recommendation

    @recommendation.setter
    def recommendation(self, recommendation: Dict):
        self._recommendation = recommendation

    @property
    def current_vis(self):
        return self._current_vis

    @current_vis.setter
    def current_vis(self, current_vis: Dict):
        self._current_vis = current_vis

    def __repr__(self):
        # TODO: _repr_ gets called from _repr_html, need to get rid of this call
        return ""

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
        # self.get_SQL_cardinality()
        for attribute in self.columns:
            if self.data_type_lookup[attribute] == "quantitative":
                self._min_max[attribute] = (
                    self[attribute].min(),
                    self[attribute].max(),
                )

    def get_SQL_attributes(self):
        if "." in self.table_name:
            table_name = self.table_name[self.table_name.index(".") + 1 :]
        else:
            table_name = self.table_name
        query = f"SELECT column_name FROM INFORMATION_SCHEMA.COLUMNS where TABLE_NAME = '{table_name}'"
        attributes = list(pd.read_sql(query, self.SQLconnection)["column_name"])
        for attr in attributes:
            self[attr] = None

    def get_SQL_cardinality(self):
        cardinality = {}
        for attr in list(self.columns):
            card_query = pd.read_sql(
                f"SELECT Count(Distinct({attr})) FROM {self.table_name}",
                self.SQLconnection,
            )
            cardinality[attr] = list(card_query["count"])[0]
        self.cardinality = cardinality

    def get_SQL_unique_values(self):
        unique_vals = {}
        for attr in list(self.columns):
            unique_query = pd.read_sql(
                f"SELECT Distinct({attr}) FROM {self.table_name}",
                self.SQLconnection,
            )
            unique_vals[attr] = list(unique_query[attr])
        self.unique_values = unique_vals

    def compute_SQL_data_type(self):
        data_type_lookup = {}
        sql_dtypes = {}
        self.get_SQL_cardinality()
        if "." in self.table_name:
            table_name = self.table_name[self.table_name.index(".") + 1 :]
        else:
            table_name = self.table_name
        # get the data types of the attributes in the SQL table
        for attr in list(self.columns):
            query = f"SELECT DATA_TYPE FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '{table_name}' AND COLUMN_NAME = '{attr}'"
            datatype = list(pd.read_sql(query, self.SQLconnection)["data_type"])[0]
            sql_dtypes[attr] = datatype

        data_type = {"quantitative": [], "nominal": [], "temporal": []}
        for attr in list(self.columns):
            if str(attr).lower() in ["month", "year"]:
                data_type_lookup[attr] = "temporal"
                data_type["temporal"].append(attr)
            elif sql_dtypes[attr] in [
                "character",
                "character varying",
                "boolean",
                "uuid",
                "text",
            ]:
                data_type_lookup[attr] = "nominal"
                data_type["nominal"].append(attr)
            elif sql_dtypes[attr] in [
                "integer",
                "real",
                "smallint",
                "smallserial",
                "serial",
            ]:
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

    def _append_rec(self, rec_infolist, recommendations: Dict):
        if recommendations["collection"] is not None and len(recommendations["collection"]) > 0:
            rec_infolist.append(recommendations)

    def maintain_recs(self):
        # `rec_df` is the dataframe to generate the recommendations on
        # check to see if globally defined actions have been registered/removed
        if lux.update_actions["flag"] == True:
            self._recs_fresh = False
        show_prev = False  # flag indicating whether rec_df is showing previous df or current self
        if self._prev is not None:
            rec_df = self._prev
            rec_df._message = Message()
            rec_df.maintain_metadata()  # the prev dataframe may not have been printed before
            last_event = self.history._events[-1].name
            rec_df._message.add(
                f"Lux is visualizing the previous version of the dataframe before you applied <code>{last_event}</code>."
            )
            show_prev = True
        else:
            rec_df = self
            rec_df._message = Message()
        # Add warning message if there exist ID fields
        id_fields_str = ""
        if len(rec_df.data_type["id"]) > 0:
            for id_field in rec_df.data_type["id"]:
                id_fields_str += f"<code>{id_field}</code>, "
            id_fields_str = id_fields_str[:-2]
            rec_df._message.add(f"{id_fields_str} is not visualized since it resembles an ID field.")
        rec_df._prev = None  # reset _prev

        # Check that recs has not yet been computed
        if not hasattr(rec_df, "_recs_fresh") or not rec_df._recs_fresh:
            rec_infolist = []
            from lux.action.custom import custom
            from lux.action.custom import custom_actions
            from lux.action.correlation import correlation
            from lux.action.univariate import univariate
            from lux.action.enhance import enhance
            from lux.action.filter import filter
            from lux.action.generalize import generalize
            from lux.action.row_group import row_group
            from lux.action.column_group import column_group

            if rec_df.pre_aggregated:
                if rec_df.columns.name is not None:
                    rec_df._append_rec(rec_infolist, row_group(rec_df))
                rec_df._append_rec(rec_infolist, column_group(rec_df))
            else:
                if rec_df.recommendation == {}:
                    # display conditions for default actions
                    no_vis = lambda ldf: (ldf.current_vis is None) or (
                        ldf.current_vis is not None and len(ldf.current_vis) == 0
                    )
                    one_current_vis = (
                        lambda ldf: ldf.current_vis is not None and len(ldf.current_vis) == 1
                    )
                    multiple_current_vis = (
                        lambda ldf: ldf.current_vis is not None and len(ldf.current_vis) > 1
                    )

                    # globally register default actions
                    lux.register_action("correlation", correlation, no_vis)
                    lux.register_action("distribution", univariate, no_vis, "quantitative")
                    lux.register_action("occurrence", univariate, no_vis, "nominal")
                    lux.register_action("temporal", univariate, no_vis, "temporal")

                    lux.register_action("Enhance", enhance, one_current_vis)
                    lux.register_action("Filter", filter, one_current_vis)
                    lux.register_action("Generalize", generalize, one_current_vis)

                    lux.register_action("Custom", custom, multiple_current_vis)

                # generate vis from globally registered actions and append to dataframe
                custom_action_collection = custom_actions(rec_df)
                for rec in custom_action_collection:
                    rec_df._append_rec(rec_infolist, rec)
                lux.update_actions["flag"] = False

            # Store _rec_info into a more user-friendly dictionary form
            rec_df.recommendation = {}
            for rec_info in rec_infolist:
                action_type = rec_info["action"]
                vlist = rec_info["collection"]
                if rec_df._plot_config:
                    if rec_df.current_vis:
                        for vis in rec_df.current_vis:
                            vis._plot_config = rec_df.plot_config
                    for vis in vlist:
                        vis._plot_config = rec_df.plot_config
                if len(vlist) > 0:
                    rec_df.recommendation[action_type] = vlist
            rec_df._rec_info = rec_infolist
            self._widget = rec_df.render_widget()
        # re-render widget for the current dataframe if previous rec is not recomputed
        elif show_prev:
            self._widget = rec_df.render_widget()
        self._recs_fresh = True

    #######################################################
    ############## LuxWidget Result Display ###############
    #######################################################
    @property
    def widget(self):
        if self._widget:
            return self._widget

    @property
    def exported(self) -> Union[Dict[str, VisList], VisList]:
        """
        Get selected visualizations as exported Vis List

        Notes
        -----
        Convert the _selectedVisIdxs dictionary into a programmable VisList
        Example _selectedVisIdxs :
                {'Correlation': [0, 2], 'Occurrence': [1]}
        indicating the 0th and 2nd vis from the `Correlation` tab is selected, and the 1st vis from the `Occurrence` tab is selected.

        Returns
        -------
        Union[Dict[str,VisList], VisList]
                When there are no exported vis, return empty list -> []
                When all the exported vis is from the same tab, return a VisList of selected visualizations. -> VisList(v1, v2...)
                When the exported vis is from the different tabs, return a dictionary with the action name as key and selected visualizations in the VisList. -> {"Enhance": VisList(v1, v2...), "Filter": VisList(v5, v7...), ..}
        """
        if not hasattr(self, "_widget"):
            warnings.warn(
                "\nNo widget attached to the dataframe."
                "Please assign dataframe to an output variable.\n"
                "See more: https://lux-api.readthedocs.io/en/latest/source/guide/FAQ.html#troubleshooting-tips",
                stacklevel=2,
            )
            return []
        exported_vis_lst = self._widget._selectedVisIdxs
        exported_vis = []
        if exported_vis_lst == {}:
            if self._saved_export:
                return self._saved_export
            warnings.warn(
                "\nNo visualization selected to export.\n"
                "See more: https://lux-api.readthedocs.io/en/latest/source/guide/FAQ.html#troubleshooting-tips",
                stacklevel=2,
            )
            return []
        if len(exported_vis_lst) == 1 and "currentVis" in exported_vis_lst:
            return self.current_vis
        elif len(exported_vis_lst) > 1:
            exported_vis = {}
            if "currentVis" in exported_vis_lst:
                exported_vis["Current Vis"] = self.current_vis
            for export_action in exported_vis_lst:
                if export_action != "currentVis":
                    exported_vis[export_action] = VisList(
                        list(
                            map(
                                self.recommendation[export_action].__getitem__,
                                exported_vis_lst[export_action],
                            )
                        )
                    )
            return exported_vis
        elif len(exported_vis_lst) == 1 and ("currentVis" not in exported_vis_lst):
            export_action = list(exported_vis_lst.keys())[0]
            exported_vis = VisList(
                list(
                    map(
                        self.recommendation[export_action].__getitem__,
                        exported_vis_lst[export_action],
                    )
                )
            )
            self._saved_export = exported_vis
            return exported_vis
        else:
            warnings.warn(
                "\nNo visualization selected to export.\n"
                "See more: https://lux-api.readthedocs.io/en/latest/source/guide/FAQ.html#troubleshooting-tips",
                stacklevel=2,
            )
            return []

    def remove_deleted_recs(self, change):
        for action in self._widget.deletedIndices:
            deletedSoFar = 0
            for index in self._widget.deletedIndices[action]:
                self.recommendation[action].remove_index(index - deletedSoFar)
                deletedSoFar += 1

    def set_intent_on_click(self, change):
        from IPython.display import display, clear_output
        from lux.processor.Compiler import Compiler

        intent_action = list(self._widget.selectedIntentIndex.keys())[0]
        vis = self.recommendation[intent_action][self._widget.selectedIntentIndex[intent_action][0]]
        self.set_intent_as_vis(vis)

        self.maintain_metadata()
        self.current_vis = Compiler.compile_intent(self, self._intent)
        self.maintain_recs()

        with self.output:
            clear_output()
            display(self._widget)

        self._widget.observe(self.remove_deleted_recs, names="deletedIndices")
        self._widget.observe(self.set_intent_on_click, names="selectedIntentIndex")

    def _repr_html_(self):
        from IPython.display import display
        from IPython.display import clear_output
        import ipywidgets as widgets

        try:
            if self._pandas_only:
                display(self.display_pandas())
                self._pandas_only = False
            else:
                if self.index.nlevels >= 2 or self.columns.nlevels >= 2:
                    warnings.warn(
                        "\nLux does not currently support dataframes "
                        "with hierarchical indexes.\n"
                        "Please convert the dataframe into a flat "
                        "table via `pandas.DataFrame.reset_index`.\n",
                        stacklevel=2,
                    )
                    display(self.display_pandas())
                    return

                if len(self) <= 0:
                    warnings.warn(
                        "\nLux can not operate on an empty dataframe.\nPlease check your input again.\n",
                        stacklevel=2,
                    )
                    display(self.display_pandas())
                    return
                self.history.copy_history()
                self.maintain_metadata()

                if self._intent != [] and (not hasattr(self, "_compiled") or not self._compiled):
                    from lux.processor.Compiler import Compiler

                    self.current_vis = Compiler.compile_intent(self, self._intent)

                if lux.config.default_display == "lux":
                    self._toggle_pandas_display = False
                else:
                    self._toggle_pandas_display = True

                # df_to_display.maintain_recs() # compute the recommendations (TODO: This can be rendered in another thread in the background to populate self._widget)
                self.maintain_recs()

                # Observers(callback_function, listen_to_this_variable)
                self._widget.observe(self.remove_deleted_recs, names="deletedIndices")
                self._widget.observe(self.set_intent_on_click, names="selectedIntentIndex")

                if len(self.recommendation) > 0:
                    # box = widgets.Box(layout=widgets.Layout(display='inline'))
                    button = widgets.Button(
                        description="Toggle Pandas/Lux",
                        layout=widgets.Layout(width="140px", top="5px"),
                    )
                    self.output = widgets.Output()
                    # box.children = [button,output]
                    # output.children = [button]
                    # display(box)
                    display(button, self.output)

                    def on_button_clicked(b):
                        with self.output:
                            if b:
                                self._toggle_pandas_display = not self._toggle_pandas_display
                            clear_output()
                            if self._toggle_pandas_display:
                                display(self.display_pandas())
                            else:
                                # b.layout.display = "none"
                                display(self._widget)
                                # b.layout.display = "inline-block"

                    button.on_click(on_button_clicked)
                    on_button_clicked(None)
                else:
                    warnings.warn(
                        "\nLux defaults to Pandas when there are no valid actions defined.",
                        stacklevel=2,
                    )
                    display(self.display_pandas())

        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            raise
            warnings.warn(
                "\nUnexpected error in rendering Lux widget and recommendations. "
                "Falling back to Pandas display.\n\n"
                "Please report this issue on Github: https://github.com/lux-org/lux/issues ",
                stacklevel=2,
            )
            display(self.display_pandas())

    def display_pandas(self):
        return self.to_pandas()

    def render_widget(self, renderer: str = "altair", input_current_vis=""):
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
        import luxwidget

        widgetJSON = self.to_JSON(self._rec_info, input_current_vis=input_current_vis)
        return luxwidget.LuxWidget(
            currentVis=widgetJSON["current_vis"],
            recommendations=widgetJSON["recommendation"],
            intent=LuxDataFrame.intent_to_string(self._intent),
            message=self._message.to_html(),
        )

    @staticmethod
    def intent_to_JSON(intent):
        from lux.utils import utils

        filter_specs = utils.get_filter_specs(intent)
        attrs_specs = utils.get_attrs_specs(intent)

        intent = {}
        intent["attributes"] = [clause.attribute for clause in attrs_specs]
        intent["filters"] = [clause.attribute for clause in filter_specs]
        return intent

    @staticmethod
    def intent_to_string(intent):
        if intent:
            return ", ".join([clause.to_string() for clause in intent])
        else:
            return ""

    def to_JSON(self, rec_infolist, input_current_vis=""):
        widget_spec = {}
        if self.current_vis:
            self.executor.execute(self.current_vis, self)
            widget_spec["current_vis"] = LuxDataFrame.current_vis_to_JSON(
                self.current_vis, input_current_vis
            )
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
        numVC = len(vlist)  # number of visualizations in the vis list
        if numVC == 1:
            current_vis_spec = vlist[0].render_VSpec()
        elif numVC > 1:
            pass
        return current_vis_spec

    @staticmethod
    def rec_to_JSON(recs):
        rec_lst = []
        import copy

        rec_copy = copy.deepcopy(recs)
        for idx, rec in enumerate(rec_copy):
            if len(rec["collection"]) > 0:
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
        self._pandas_only = True
        self._history.append_event("info", *args, **kwargs)
        return super(LuxDataFrame, self).info(*args, **kwargs)

    def describe(self, *args, **kwargs):
        self._pandas_only = True
        self._history.append_event("describe", *args, **kwargs)
        return super(LuxDataFrame, self).describe(*args, **kwargs)

    def groupby(self, *args, **kwargs):
        self.add_to_global_record("groupby", *args, **kwargs)
        return super(LuxDataFrame, self).groupby(*args, **kwargs)

    def add_to_global_record(self, name, *args, **kwargs):
        self._history.append_event(name, *args, **kwargs)
        LuxDataFrame.recent_record = self._history
