import streamlit as st
import util
import config
import llm_interface
import streamlit.components.v1 as components


def semantics_tab():
    
    if not(config.prompt_flag):
        st.error("No prompt defined!")
    
    else:
        with st.expander("LLM Prompt and generated Label", expanded=False):
            prompt_form = st.form(key='prompt_form')
            config.prompt_text = llm_interface.generate_prompt(config.prompts)


            prompt_statement = prompt_form.text_area("Prompt:", value=config.prompt_text)
            prompt_submitted = prompt_form.form_submit_button("Generate Concept Relationship Label")

            if(prompt_submitted):
                response = []
                while(not response or len(response[0]) != 3):
                    response = llm_interface.generate_label(config.model, config.prompt_text, [config.origin_concept, config.destination_concept])
                
                st.write(response)
                config.concepts_relationship_label = response[0][2]
                util.write_concept_relationship()
                
              
            if(st.button("Accept generated Concept Relationship Label")):
                config.graph_add_flag = True
                config.relationship_label_flag = True
                
                util.add_to_concept_list()
                st.write(config.concepts_list)
                
            
        with st.expander("Graph", expanded=True):
            if(config.NxGraph is None):
                util.generate_graph()
            
            if(config.graph_add_flag):
                util.add_node()
                config.graph_add_flag = False

            util.plot_graph()
            
        
        with st.expander("LLM Prompt and generated Node-Features", expanded=True):
            
            
            
        

            