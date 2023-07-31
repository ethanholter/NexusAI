import json

# ----------------------------------
# TOOL CLASS
# ----------------------------------

class Tool:
    name = ""
    description = ""
    required = []

    # {"[VARIABLE NAME 1]": {"type": "","description": ""}, "[VARIABLE NAME 2]": {"type": "","description": ""}}
    properties = dict()
    callback = None

    # TODO add error checking
    def __init__(self, name, description, callback, required, properties):
        self.name = name
        self.description = description
        self.required = required
        self.callback = callback
        
        self.properties = properties
        if not self.properties:
            self.properties = dict()

    def run(self, **kwargs):
        self.callback(**kwargs)

    def getName(self):
        return self.name

    def getDescription(self):
        return self.description

    def getParameters(self):
        return {
            "type": "object",
            "required": self.required,
            "properties": self.properties,
        }

# ----------------------------------
# TOOLKIT CLASS
# ----------------------------------

class Toolkit:
    tools: list[Tool]
    tool_name_map: dict

    def __init__(self):
        self.tools = []
        self.tool_name_map = {}

    def getToolJSON(self):
        toolList = []
        for tool in self.tools:
            toolList.append(
                {
                    "name": tool.getName(),
                    "description": tool.getDescription(),
                    "parameters": tool.getParameters(),
                }
            )
        return toolList

    def setTools(self, tools):
        self.tools = tools
        for tool in tools:
            self.tool_name_map[tool.name] = tool.callback
    
    def run(self, tool_name, **kwargs):
        try:
            result = self.tool_name_map[tool_name](**kwargs)
        except KeyError as e:
            print(tool_name + " is not a valid tool")
            print(e)
            return "Failed to perform action"
        except Exception as e:
            print(e)
            return "Failed to perform action"
        
        if result:
            return result
        else:
            return "Success"
        

# ----------------------------------
# TOOLKIT FUNCTIONS
# ----------------------------------

def sample_tool(query):
    print("1")

def sample_tool_2(query):
    print("2")
    
# ----------------------------------
# MAIN FUNCTION
# ----------------------------------

if __name__ == "__main__":
    toolkit = Toolkit()

    toolkit.setTools(
        [
            Tool(
                name="sample_tool",
                description="This does nothing",
                required=["query"],
                callback=sample_tool,
                properties={
                    "query": {
                        "type": "string",
                        "description": "this does literally nothing lol",
                    }
                },
            ),
            Tool(
                name="sample_tool_2",
                description="This does nothing",
                required=["query"],
                callback=sample_tool_2,
                properties={
                    "query": {
                        "type": "string",
                        "description": "this does literally nothing lol",
                    }
                },
            )
        ]
    )
    
    print(toolkit.getToolJSON())
    toolkit.run("sample_tool_1", query="test")
    
    
