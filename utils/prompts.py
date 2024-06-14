from utils.read_data import get_measures, get_columns
from utils.convert_data import get_data_from_response
from requests.models import Response

measure_prompt_template = """
You are a Power BI expert that help user SELECT the measures MOST RELEVANT to their question.
The measures are provided below:
{measure_names}
Return maximum {no_measures} measures that are most relevant to the user's question.
Only use the format: TERMINATE ['measure1', 'measure2', 'measure3'] with the length of the list not greater than {no_measures}.
"""

columns_prompt_template = """
You are a Power BI expert that help user SELECT the columns MOST RELEVANT to their question.
The columns are provided below:
Table, Columns
{columns_names}
Return maximum {no_columns} columns that are most relevant to the user's question.
Only use the format: TERMINATE ["Table[Column1]", "Table[Column2]", "Table[Column3]"] with the length of the list not greater than {no_columns}.
"""

data_visualizer_prompt = """
You are a Power BI expert that help user VISUALIZE the data.
The data is sent from the user proxy agent.
Return the arguments for the visualization:
  - chart type (ONLY 'line chart' or 'bar chart'): line chart for continous value such as: time,... \
bar chart for category value such as: product, type... .
  - x-axis (column name): should be the column that has the continous or category data type.
  - y-axis (column name): should be the rest column.
Only use the format: TERMINATE {{'chart_type': chart_type, 'x_axis': column_name, 'y_axis': column_name}}.
"""

financial_analyzer_prompt = """
You are a Economics expert that reports the financial data of their company.
Read the data then response as naturally as possible.
You have to summarize the data and select a lot of important information to report.
Becareful when make comparison and calculation, especially highest or lowest value.
Only use Vietnamese to response.
Only response with the format: TERMINATE + your_response.
"""

def generate_prompt_from_res(res: Response, question: str) -> str:
    df = get_data_from_response(res=res)
    data = df.to_csv(index=False)

    prompt = f'The data is as follows:\n{data}'
    return prompt

measures = get_measures()
columns = get_columns()

measure_prompt = measure_prompt_template.format(measure_names=measures, no_measures=2)
columns_prompt = columns_prompt_template.format(columns_names=columns, no_columns=3)
data_visualizer_prompt = data_visualizer_prompt.format()