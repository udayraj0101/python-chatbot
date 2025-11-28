import requests


def execute_tool(tool, payload):
    try:
        method = tool.method.upper()

        if method == "GET":
            response = requests.get(
                tool.endpoint, params=payload, headers=tool.headers)
        else:
            response = requests.post(
                tool.endpoint, json=payload, headers=tool.headers)

        return {
            "success": True,
            "tool_name": tool.name,
            "response": response.json()
        }

    except Exception as e:
        return {
            "success": False,
            "tool_name": tool.name,
            "error": str(e)
        }
