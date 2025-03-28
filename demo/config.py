from sqlalchemy import create_engine
import pandas as pd

#connection
engine = create_engine('postgresql://postgres:postgres@localhost:5432/incordb') 
connection = engine.connect()

#flags
concepts_flag = None
prompt_flag = None
relationship_label_flag = None
graph_flag = None
graph_add_flag = None

#table
df_query_result = None
table_names_query_result = None
table_columns_query_result = None
table = None

#Graph
NxGraph = None

#concepts
origin_concept = None
destination_concept = None

#prompt
prompt_text = None

#llm model
model = "gemma:latest"
prompts = "no_shot_complex_prompt"

#relationship label
concepts_relationship_label = " relates to " #placeholder, mudar depois!!!!
concepts_list = []