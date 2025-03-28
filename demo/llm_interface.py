from langchain_core.prompts import ChatPromptTemplate  
from langchain_ollama.llms import OllamaLLM
import pandas as pd
import re
from pathlib import Path
import subprocess
import config

templates = {
"no_shot_simple_prompt" :
"""
Contex: 
find a word to descibre the relationship among a pair of entitys 
Pair: {question}

you should answer like this:
Pair: [repeat the given Pair]
reasoning: [write how you got to the answer]
Answer: [first word of the pair(as you were given), second word(as you were given),relationship among them] 
""",
"no_shot_complex_prompt" :
"""
Contex: 
A semantic network is a knowledge base that represents semantic relations between concepts in a network, you will be given two words from relatade to medice and have to inffer the best word to describe their relationship among them for a semantic network

Pair: {question}

you should answer like this:
Pair: [repeat the given Pair]
reasoning: [write how you got to the answer]
Answer: [first word of the pair(as you were given), second word(as you were given),relationship among them] 

""",
"simple_prompt" :
""""
Contex: 
A semantic network is a knowledge base that represents semantic relations between concepts in a network, you will be given two words from a medical context and have to inffer the best word to describe their relationship among them for a semantic network
you should answer like this:
Pair: [repeat the given Pair]
reasoning: [write how you got to the answer]
Answer: [first word of the pair(as you were given), second word(as you were given),relationship among them] 

example:
Pair: [human,apple]
Reasoning: in our world humans use to eat apples
Answer: human,apple,eats

example2:
Pair: [Paris,France]
Reasoning: paris is the capital of France 
Answer: paris,france,capital

example3:
Pair: [fire,Wood]
Reasoning: we know that when fire and wood get together the wood burns
Answer: fire,wood,burns

example3:
Pair: [Wood,fire]
Reasoning: we know that when fire and wood get together the fire gets bigger
Answer: wood,fire,strengthens

Pair to answer: {question}

""",
"complex_prompt" :
""""
Contex: 
find a word to descibre the relationship among a pair of entitys 

you should answer like this:
Pair: [repeat the given Pair]
reasoning: [write how you got to the answer]
Answer: [first word of the pair(as you were given), second word(as you were given),relationship among them] 

example:
Pair: [human,apple]
Reasoning: in our world humans use to eat apples
Answer: human,apple,eats

example2:
Pair: [Paris,France]
Reasoning: paris is the capital of France 
Answer: paris,france,capital

example3:
Pair: [fire,Wood]
Reasoning: we know that when fire and wood get together the wood burns
Answer: fire,wood,burns

example3:
Pair: [Wood,fire]
Reasoning: we know that when fire and wood get together the fire gets bigger
Answer: wood,fire,strengthens

Pair to answer: {question}

"""
}

# concept_pairs = [["person_id", "drug_concept_id"],
#     ["drug_concept_id", "person_id"],
#     ["ingredient_concept_id", "drug_concept_id"],
#     ["drug_concept_id", "ingredient_concept_id"],
#     ["observation_period_id", "person_id"],
#     ["person_id", "observation_period_id"],
#     ["person_id", "procedure_occurrence_id"],
#     ["procedure_occurrence_id", "person_id"],
#     ["person_id", "visit_occurrence"]]

def Verify_LLM_Existence(LLM_Name:list):
    result = subprocess.run(["ollama","list"], capture_output=True, text=True)
    result = result.stdout.split()
    # if LLM_Name not in result:
    #     print(f"Some requirements were not satisfied LLM {LLM_Name} is not locally downloaded")
    #     return 0 
    return 1

def generate_prompt(prompt_type):
    # for index,pairs in enumerate(List_pairs):
    template = templates[prompt_type]
    prompt = ChatPromptTemplate.from_template(template)

    return prompt

def generate_label(model, prompt, concept_pair):
    current_model = OllamaLLM(model=f"{model}")
    chain = prompt | current_model
    response = chain.invoke({"question":concept_pair})

    #Encontrar qualquer linha que começa com "Answer"
    regex = r"^Answer\b.*"
    response = re.findall(regex, response, re.MULTILINE)

    # Remover o prefixo "Answer:"
    regex1 = r"^Answer:\s*"
    response = [re.sub(regex1, "", r) for r in response]

    # Substituir palavras por elas mesmas entre aspas
    regex2 = r"\b\w+\b"
    response = [re.findall(r'"(.*?)"', re.sub(regex2, r'"\g<0>"', r)) for r in response]
    return response



# def Evoke_Models(model:str,List_pairs:list,prompt_type:str):
#     responses = [""] * len(List_pairs)    

#     for index,pairs in enumerate(List_pairs):
 
#         if Verify_LLM_Existence(model):
#             template = templates[prompt_type]
#             prompt = ChatPromptTemplate.from_template(template)
#             current_model = OllamaLLM(model=f"{model}")

#             chain = prompt | current_model

#             responses[index] = chain.invoke({"question":pairs})
#             # regex = r"^Answer\b.*"
#             # responses[index] = re.findall(regex,responses[index],re.MULTILINE)
#             # regex1 = r"^Answer:\s*"
#             # responses[index] = [re.sub(regex1,"",i) for i in responses[index]]
#             # regex2 = r"\b\w+\b"
#             # responses[index] = [re.findall(r'"(.*?)"',re.sub(regex2,r'"\g<0>"',i)) for i in responses[index]]
#     print(responses)
            

# def main_llm():
#     models = "gemma:2B"
#     prompts = "no_shot_complex_prompt"
#     Evoke_Models(model=models, prompt_type=prompts, List_pairs=concept_pairs)
