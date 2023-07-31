import json
import os
import sys
import warnings

import openai

from ..toolkits.spotify_toolkit import spotify_toolkit

system_prompt = """
You are a secondary language model designed to supplement a seperate main model. Your job is to receive instructions from the main model and then execute a function based on those instructions. You will always call a function. If a function has the parameter 'dummy_property' then provide no parameter.
"""

class Agent:
    def __init__(self, model="gpt-3.5-turbo",verbose=False):
        self.model = model
        self.temp = 0
        self.max_iterations = 4
        self.system_prompt = system_prompt
        self.functions = ""
        self.messageBuffer = [{"role": "system", "content": self.system_prompt}]
        self.verbose = verbose


    # Tells the model which functions it is allowed to call if needed and how to use them
    def setFunctions(self, functions):
        self.functions = functions
        
    def run(self, toolkit_name, query):
        # if toolkit_name == "home_toolkit":
        #     self.setFunctions(home_toolkit.getToolJSON())
        
        if toolkit_name == "spotify_toolkit":
            self.setFunctions(spotify_toolkit.getToolJSON())
        
        self.messageBuffer.append({"role": "user", "content": query})
        response = openai.ChatCompletion.create(
            model=self.model,
            stream=False,
            temperature=self.temp,
            messages=self.messageBuffer,
            functions=self.functions,
            function_call="auto",
        )
        
        choice = response["choices"][0]
        message = choice.get("message")
        content = message.get("content")
        function_call = message.get("function_call")
        
        if not function_call:
            raise (Exception)
        
        
        
        function_name = function_call["name"]
        function_args = json.loads(message["function_call"]["arguments"])
        
        
        # if toolkit_name == "home_toolkit":
        #     home_toolkit.callFunction(function_name, function_args)
        
        if toolkit_name == "spotify_toolkit":
            result = spotify_toolkit.run(function_name, **function_args)
        
        
        if self.verbose:
            print(response)
        
        return result
        