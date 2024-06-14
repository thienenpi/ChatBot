from typing import Dict, List, Tuple, Union, Optional

class QueryGenerator:
    # init
    def __init__(self):
        pass
    
    def _generate_query(
        self,
        measure: Union[str, List[str]],
        groupby_columns: List[Tuple[str, str]],
        filters: Dict[Tuple[str, str], List[str]],
        num_rows: Optional[int] = None,
        verbose: int = 0,
        ) -> str:
        # we should always quote table names (e.g. Date/Calendar as table name will fail without quotes)
        groupby_string = ", ".join(f"'{col[0]}'[{col[1]}]" for col in groupby_columns)

        measure_lst = measure if isinstance(measure, list) else [measure]
        measure_string = ", ".join(f'\"{m}\", CALCULATE([{m}])' for m in measure_lst)

        filter_clauses = []
        for table_col, filter_list in filters.items():
            table_name = table_col[0]
            col_name = table_col[1]
            # DAX requires the "IN" items to use double quotes within braces:
            filter_vals = "{" + ", ".join([f'\"{val}\"' for val in filter_list]) + "}"
            # Create individual FILTER functions for every filter specified by user (table names always quoted with single quotes)
            # See https://learn.microsoft.com/en-us/dax/filter-function-dax)
            filter_clauses.append(f"FILTER('{table_name}', '{table_name}'[{col_name}] IN {filter_vals})")
        # Final String: FILTER('Table1', 'Table1'[Col1] IN {"X", "Y"}), FILTER('Table2', 'Table2'[Col2] IN {"A"})
        filter_string = ", ".join(filter_clauses)

        summarize_columns = 'SUMMARIZECOLUMNS('
        if len(groupby_string) > 0:
            summarize_columns += f'{groupby_string}, '
        if len(filter_string) > 0:
            summarize_columns += f"{filter_string}, "
        summarize_columns += f"{measure_string})"

        if num_rows:
            dax_string = f"EVALUATE TOPN({num_rows}, {summarize_columns})"
        else:
            dax_string = f"EVALUATE {summarize_columns}"

        return dax_string

    @staticmethod
    def _parse_column_reference(column_spec: str) -> Tuple[Optional[str], str]:
        table_name = None
        column_name = column_spec
        if column_spec.endswith(']'):
            column_idx = column_spec.find('[')
            if column_idx >= 0:
                column_name = column_spec[column_idx + 1:-1]
                table_name = column_spec[:column_idx]
                if table_name.startswith("'") and table_name.endswith("'"):
                    table_name = table_name[1:-1]

        return table_name, column_name

    def _parse_fully_qualified_column(self, column_spec: str) -> Tuple[str, str]:
        # This method enforces that table name is specified, which is a requirement for
        # DAX/REST calls in groupby and filters.
        table_name, column_name = self._parse_column_reference(column_spec)

        if table_name is None or table_name == "":
            raise ValueError(f"Cannot parse table name from '{column_spec}'")

        return table_name, column_name

    def generate_query(
        self,
        measure: Union[str, List[str]],
        groupby_columns: Optional[List[str]] = None,
        filters: Optional[Dict[str, List[str]]] = None,
        fully_qualified_columns: Optional[bool] = None,
        num_rows: Optional[int] = None,
        verbose: int = 0
    ) -> str:
        if groupby_columns is None:
            groupby_columns = []
        if not isinstance(groupby_columns, list):
            raise TypeError(f"Unexpected type {type(groupby_columns)} for \"groupby_columns\": not a list")
        parsed_groupby = []
        for g in groupby_columns:
            if not isinstance(g, str):
                raise TypeError(f"Unexpected type {type(g)} for \"groupby_columns\" element: not a str")
            parsed_groupby.append(self._parse_fully_qualified_column(g))

        if filters is None:
            filters = {}
        parsed_filters = {}
        for table_col, filter_lst in filters.items():
            if not isinstance(table_col, str):
                raise TypeError(f"Unexpected type {type(table_col)} for \"filters\" key: not a str")
            if not isinstance(filter_lst, list):
                raise TypeError(f"Unexpected type {type(filter_lst)} for \"filters\" value: not a list")
            parsed_filters[self._parse_fully_qualified_column(table_col)] = filter_lst

        columns = [g[1] for g in parsed_groupby]
        naming_conflict = len(set(columns)) != len(columns)
        if naming_conflict and fully_qualified_columns is False:
            dupl_columns = [col for col in columns if columns.count(col) > 1]
            raise ValueError(f"Multiple columns with the name(s) '{set(dupl_columns)}' given. Use 'fully_qualified_columns=True' to avoid conflicts.")
        if fully_qualified_columns is None:
            fully_qualified_columns = True if naming_conflict else False
            if verbose > 1:
                print(f"Setting fully_qualified_columns to {fully_qualified_columns}")

        if isinstance(measure, list):
            measure_lst = measure
        elif isinstance(measure, str):
            measure_lst = [measure]
        else:
            raise TypeError(f"Unexpected type {type(measure)} for \"measure\": not a list or str")

        parsed_measures = []
        for m in measure_lst:
            if not isinstance(m, str):
                raise TypeError(f"Unexpected type {type(m)} for \"measure\" element: not a str")
            # strip [] from each measure
            parsed_measures.append(m[1:-1] if m.startswith("[") and m.endswith("]") else m)

        return self._generate_query(measure=parsed_measures, groupby_columns=parsed_groupby, filters=parsed_filters, num_rows=num_rows, verbose=verbose)