from swarm import Agent, Swarm
import time

# Initialize the Swarm
client = Swarm()

# Define the agents
agent_a = Agent(
    name="Agent A",
    instructions="You are arguing in favor of the given topic. Provide concise, logical arguments to support your position.",
    llm="gpt-4"
)

agent_b = Agent(
    name="Agent B",
    instructions="You are arguing against the given topic. Provide concise, logical arguments to oppose the given position.",
    llm="gpt-4"
)

agent_c = Agent(
    name="Agent C",
    instructions="You are the moderator. Ensure the debate remains civil and on-topic. Provide brief summaries and ask short, probing questions to both sides.",
    llm="gpt-4"
)

# Function to run the debate
def run_debate(topic):
    messages = [{"role": "system", "content": f"The debate topic is: {topic}. This is a 1-minute debate."}]
    start_time = time.time()
    
    while time.time() - start_time < 60:  # Run for 1 minute
        # Agent A's turn
        response_a = client.run(agent=agent_a, messages=messages)
        messages.append({"role": "assistant", "content": f"Agent A: {response_a.messages[-1]['content']}"})
        print(f"Agent A: {response_a.messages[-1]['content']}\n")
        
        # Agent B's turn
        response_b = client.run(agent=agent_b, messages=messages)
        messages.append({"role": "assistant", "content": f"Agent B: {response_b.messages[-1]['content']}"})
        print(f"Agent B: {response_b.messages[-1]['content']}\n")
        
        # Moderator's turn
        response_c = client.run(agent=agent_c, messages=messages)
        messages.append({"role": "assistant", "content": f"Moderator: {response_c.messages[-1]['content']}"})
        print(f"Moderator: {response_c.messages[-1]['content']}\n")
        
        if time.time() - start_time >= 60:
            break
    
    print("Debate time has ended.")

# Get user input for the debate topic
debate_topic = input("Enter the debate topic: ")

# Run the debate
run_debate(debate_topic)