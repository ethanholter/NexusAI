import json
import os
import sys
import warnings

import openai

from ELTTS import speakText

openai.api_key = os.getenv("OPENAI_API_KEY")

DISABLE_TTS = True
if DISABLE_TTS: 
    warnings.warn("Text-to-speech is currently disabled to save API usage minutes", UserWarning)

# ---------------------------------
# Main Class
# ---------------------------------


class Assistant:
    def __init__(self, model="gpt-3.5-turbo", system_prompt="",verbose=False):
        self.model = model
        self.temp = 0.5
        self.max_iterations = 4
        self.system_prompt = system_prompt
        self.functions = ""
        self.messageBuffer = [{"role": "system", "content": self.system_prompt}]
        self.verbose = verbose

    # The system prompt tells the language model how it is supposed to behave. e.g. "you are a helpful assistant"
    def setSystemPrompt(self, system_prompt):
        self.system_prompt = system_prompt
        self.messageBuffer[0] = {"role": "system", "content": self.system_prompt}

    # Tells the model which functions it is allowed to call if needed and how to use them
    def setFunctions(self, functions):
        self.functions = functions

    # Takes a message buffer (every previous message) and completes the next message
    def completeChat(self, messageBuffer):
        response = openai.ChatCompletion.create(
            model=self.model,
            stream=False,
            temperature=self.temp,
            messages=messageBuffer,
            functions=self.functions,
            function_call="auto",
        )
        return response

    # Sometimes the AI will want to call functions.
    # In this scenario multiple requests need to be made to relay the resulting information back to the model
    def processInput(self, userInput):
        iterations = 0
        result = ""
        self.messageBuffer.append({"role": "user", "content": userInput})

        while True:
            # limit number api requests to prevent accidental infinite looping
            if iterations > self.max_iterations:
                raise (Exception, "max iterations reached")

            # get response from api
            response = self.completeChat(self.messageBuffer)
            choice = response["choices"][0]
            message = choice.get("message")
            content = message.get("content")
            
            if self.verbose:
                print(response)

            # API will respond with either a message or a function call
            # If a message is received then print the message
            if content:
                self.messageBuffer.append({"role": "assistant", "content": content})
                result += content

                # This means the model is done speaking
                if response["choices"][0]["finish_reason"] == "stop":
                    break

            # If a function is called then execute the function and add it to the messages
            # TODO add error handeling because the language model sucks at following instructions
            else:
                function_call = message.get("function_call")
                if function_call:
                    function_name = function_call["name"]
                    function_args = json.loads(message["function_call"]["arguments"])

                if not function_call:
                    raise (Exception)


                self.messageBuffer.append(
                    {"role": "function", "name": function_name, "content": "Action Successful"}
                )
           
        return result


# For testing purposes. simple conversation in command line
if __name__ == "__main__":
    assistant = Assistant(verbose=True)
    
    with open(f"{sys.path[0]}/../system_prompt.txt") as system_prompt:
        assistant.setSystemPrompt(system_prompt.read())
    
    with open(f"{sys.path[0]}/../toolkits.json") as functions:
        assistant.setFunctions(json.load(functions))

    while True:
        try:
            userInput = input("User: ")
            
            if not userInput:
                break
            
            response = assistant.processInput(userInput)
            print("Jarvis: " + response)
            
            if not DISABLE_TTS:
                speakText(response)
        except KeyboardInterrupt:
            break