import json
import os
import sys
import warnings

import openai

MODEL = "gpt-3.5-turbo"
TEMP = 0.1

system_prompt = """
You are a secondary language model designed to supplement a seperate main model. Your job is to receive instructions from the main model and then execute a function based on those instructions. You will always call a function. 
"""

class Agent:
    def __init__(self, model="gpt-3.5-turbo",verbose=False):
        self.model = model
        self.temp = 0.5
        self.max_iterations = 4
        self.system_prompt = system_prompt
        self.functions = ""
        self.messageBuffer = [{"role": "system", "content": self.system_prompt}]
        self.verbose = verbose


    # Tells the model which functions it is allowed to call if needed and how to use them
    def setFunctions(self, functions):
        self.functions = functions
        
    def run(query):
        