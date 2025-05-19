from agent import agent_graph

print("Agent is ready. Type your request.")
while True:
    user_input = input(">>> ")
    if user_input.lower() in ['exit', 'quit']:
        break

    try:
        result = agent_graph.invoke({"input": user_input})
        print(result.get("output", "No response"))
    except Exception as e:
        print("Error:", e)
 