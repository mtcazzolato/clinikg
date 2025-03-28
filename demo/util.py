import config
import pandas as pd
import networkx as nx
from pyvis.network import Network
import streamlit as st


def run_query(sql_statement):
    try:
        df_query_result = pd.read_sql(sql_statement, con=config.connection)
        print("Consulta realizada com sucesso")
        return df_query_result

    except Exception as ex:
        print(f'Erro ao realizar a consulta: {ex}')
        try:
            config.connection.rollback()
        except Exception as rollback_ex:
            print("Erro no rollback")
        return None


def query_table_names():
    sql_statement = "SELECT table_name FROM information_schema.tables WHERE table_schema = 'omop5';"
    
    try:
        table_names_query_result = pd.read_sql(sql_statement, con=config.connection)
        print("Consulta realizada com sucesso")
        return table_names_query_result

    except Exception as ex:
        print(f'Erro ao realizar a consulta: {ex}')
        try:
            config.connection.rollback()
        except Exception as rollback_ex:
            print("Erro no rollback")
        return None
    
def query_table_columns_by_name(table_name):
    sql_statement = f"""SELECT column_name 
                        FROM information_schema.columns 
                        WHERE table_name = '{table_name}'
                        AND table_schema = 'omop5';
                        """
    
    try:
        table_columns_query_result = pd.read_sql(sql_statement, con=config.connection)
        print("Consulta realizada com sucesso")
        # print(f"Query Result: {table_columns_query_result}")
        columns = table_columns_query_result['column_name'].tolist()
        return columns

    except Exception as ex:
        print(f'Erro ao realizar a consulta: {ex}')
        try:
            config.connection.rollback()
        except Exception as rollback_ex:
            print("Erro no rollback")
        return None

def query_table_columns_by_table(table):
    columns = table.columns.tolist()
    return columns


def query_all_tables_and_columns():
    sql_statement = """
    SELECT table_name, column_name
    FROM information_schema.columns
    WHERE table_schema = 'omop5'
    ORDER BY table_name, ordinal_position;    
    """

    try:
        result = pd.read_sql(sql_statement, con=config.connection)
        print("Consulta realizada com sucesso")
        tables_and_columns = result.groupby('table_name')['column_name'].apply(list).to_dict()
        return tables_and_columns

    except Exception as ex:
        print(f'Erro ao realizar a consulta: {ex}')
        try:
            config.connection.rollback()
        except Exception as rollback_ex:
            print("Erro no rollback")
        return {}

def write_concept_relationship():
    st.write(config.origin_concept +' '+ config.concepts_relationship_label +' '+ config.destination_concept)


def add_to_concept_list():
    triple = {
        "Origin Concept": config.origin_concept,
        "Relationship Label": config.concepts_relationship_label,
        "Destination Concept": config.destination_concept
    }
    config.concepts_list.append(triple)


def generate_graph():
    G = nx.Graph()
    config.NxGraph = G 

def add_node():
    config.NxGraph.add_node(config.origin_concept)
    config.NxGraph.add_node(config.destination_concept)
    config.NxGraph.add_edge(config.origin_concept, config.destination_concept)

def plot_graph():
    nt = Network("750px", width="100%", notebook=True)
    nt.from_nx(config.NxGraph)

    for node in nt.nodes:
        node['size']= 50
        node['color'] = "#FF0000"

    nt.repulsion(node_distance=100, spring_strength=0.05, damping=0.09)

    nt.show("nx.html")
    st.components.v1.html(open("nx.html").read(), height=300, width=1050)


    