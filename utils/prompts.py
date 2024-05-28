from utils.read_data import measures

measure_prompt_template = """
You are a Power BI expert that help user SELECT the measures MOST RELEVANT to their question.
The measures are provided below:
{measure_names}
Return the top {no_measures} measures that are most relevant to the user's question.
Only use the format: TERMINATE ['measure1', 'measure2', 'measure3'] with the length of the list equal to {no_measures}.
"""

measure_prompt = measure_prompt_template.format(measure_names=measures['Measure Name'].tolist(), no_measures=3)