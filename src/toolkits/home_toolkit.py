def toggleLights(newState: bool):
    print("Lights now set to " + newState)
    
def toggleAC(newState: bool):
    print("AC now set to " + newState)
    
def getTemp(room: str):
    return "73 F"


class Tool:
    def __init__(self, name, desc, func, parameters):
        self.name = name
        self.desc = desc
        self.func = func
        self.parameters = parameters

functions = [
    Tool(
        name="toggle_lights",
        desc="Turns the lights on/off",
        func=toggleLights,
        parameters= {
            "type": "object",
            "required": ["newState"],
            "properties": {
                "newState": {
                    "type": "boolean",
                    "description": "True for on, False for off"
                }
            }
        }
    ),
    Tool(
        name="toggleAC",
        desc="Turns the AC on/off",
        func=toggleLights,
        parameters={
            "type": "object",
            "required": ["newState"],
            "properties": {
                "newState": {
                    "type": "boolean",
                    "description": "True for on, False for off"
                }
            }
        }
    )
]