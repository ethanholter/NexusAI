def toggleLights(newState):
    print("\x1b[1;36m" + "Lights now set to " + str(newState['newState']) + "\x1b[0m")
    
def toggleAC(newState: bool):
    print("AC now set to " + newState)
    
def getTemp(room: str):
    return "73 F"

functionMap = {
    "toggle_lights":toggleLights,
    "toggle_AC": toggleAC,
    "get_temp":getTemp
    }

functions = [
        {
        "name": "toggle_lights",
        "description": "Turns the lights on/off",
        "parameters": {
            "type": "object",
            "required": ["newState"],
            "properties": {
                "newState": {
                    "type": "boolean",
                    "description": "True for on, False for off"
                }
            }
        }
        },
    {
        "name": "toggle_AC",
        "description": "Turns the AC on/off",
        "parameters": {
            "type": "object",
            "required": ["newState"],
            "properties": {
                "newState": {
                    "type": "boolean",
                    "description": "True for on, False for off"
                }
            }
        }
    }
]

def callFunction(name, args):
    functionMap[name](args)