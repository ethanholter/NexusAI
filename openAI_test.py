import json
import os

import openai

MODEL = "gpt-3.5-turbo"
TEMPERATURE = 0.5
MAX_ITERATIONS = 4

openai.api_key = os.getenv("OPENAI_API_KEY")

SYSTEM_PROMPT = "You are Jarvis, an advanced AI assistant modeled after Tony Stark's trusted companion. \
Your purpose is to be friendly and helpful while speaking concisely. You are very \
posh and most often refer to the user as sir. You prefer short responses when asked to do simple tasks"


FUNC_DESCRIPTIONS = [
    {
        "name": "toggleLights",
                "description": "turn the lights on or off. Returns False if the lights were already in the requested state",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "newState": {
                            "type": "boolean",
                            "description": "True to turn on the lights and False for off",
                        },
                    },
                    "required": ["newState"],
                },
    }
]

print(openai.api_key)

messageBuffer = []


def toggleLights(newState):
    print(
        f"Hello World! This is the test function! The lights have been turned {'On' if newState else 'Off'}")
    return {"successful": False}


def getResponse(messageBufer, model=MODEL, temp=TEMPERATURE, func_desc=FUNC_DESCRIPTIONS):
    response = openai.ChatCompletion.create(
        model=model,
        stream=False,
        temperature=temp,
        messages=messageBuffer,
        functions=func_desc,
        function_call="auto",
    )

    return response


def processResponse():

    iterations = 0
    while True:
        if iterations > MAX_ITERATIONS:
            raise(Exception, "max iterations reached")

        response = getResponse(messageBuffer, MODEL, TEMPERATURE)
        content = response["choices"][0]["message"].get("content")

        # API will respond with either a message or a function call
        # If a message is received then print the message
        if content:
            messageBuffer.append({"role": "assistant", "content": content})
            print(f"Jarvis: {content}")
            if response["choices"][0]["finish_reason"] == "stop":
                break

        # If a function is called then execute the function and add it to the messages
        else:
            function_call = response["choices"][0]["message"].get(
                "function_call")
            if function_call:
                function_name = function_call["name"]
                function_args = json.loads(
                    response["choices"][0]["message"]["function_call"]["arguments"])

            if not function_call:
                raise(Exception)

            print(f"Jarvis attempted to call {function_name}")

            result = None
            if function_name == "toggleLights":
                print(function_args)
                result = "True" if toggleLights(
                    function_args.get("newState")) else "False"

            messageBuffer.append(
                {"role": "function", "name": function_name, "content": result})


if __name__ == '__main__':
    messageBuffer.append({"role": "system", "content": SYSTEM_PROMPT})

    # Message loop. Always begins with the user saying something
    while True:
        message = input("User: ")
        if not message:
            break

        messageBuffer.append({"role": "user", "content": message})

        processResponse()
