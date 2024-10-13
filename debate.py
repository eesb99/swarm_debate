from swarm import Agent, Swarm
import time
import tiktoken

# Initialize the Swarm
client = Swarm()

# Define the agents
agent_a = Agent(
    name="Agent A",
    instructions="You are arguing in favor of the given topic. Provide concise, logical arguments to support your position.",
    llm="gpt-4o"
)

agent_b = Agent(
    name="Agent B",
    instructions="You are arguing against the given topic. Provide concise, logical arguments to oppose the given position.",
    llm="gpt-4o"
)

agent_c = Agent(
    name="Agent C",
    instructions="You are the moderator. Ensure the debate remains civil and on-topic. Provide brief summaries and ask short, probing questions to both sides.",
    llm="gpt-4o"
)

# Function to count tokens
def count_tokens(text, model="gpt-3.5-turbo"):
    encoding = tiktoken.encoding_for_model(model)
    return len(encoding.encode(text))

# Function to run the debate
def run_debate(topic):
    messages = [{"role": "system", "content": f"The debate topic is: {topic}. This is a 1-minute debate."}]
    start_time = time.time()
    total_tokens = count_tokens(messages[0]["content"])  # Count initial message tokens
    
    while time.time() - start_time < 60:  # Run for 1 minute
        # Agent A's turn
        response_a = client.run(agent=agent_a, messages=messages)
        response_content = response_a.messages[-1]['content']
        messages.append({"role": "assistant", "content": f"Agent A: {response_content}"})
        print(f"Agent A: {response_content}\n")
        total_tokens += count_tokens(response_content)  # Count response tokens
        
        # Agent B's turn
        response_b = client.run(agent=agent_b, messages=messages)
        response_content = response_b.messages[-1]['content']
        messages.append({"role": "assistant", "content": f"Agent B: {response_content}"})
        print(f"Agent B: {response_content}\n")
        total_tokens += count_tokens(response_content)  # Count response tokens
        
        # Moderator's turn
        response_c = client.run(agent=agent_c, messages=messages)
        response_content = response_c.messages[-1]['content']
        messages.append({"role": "assistant", "content": f"Moderator: {response_content}"})
        print(f"Moderator: {response_content}\n")
        total_tokens += count_tokens(response_content)  # Count response tokens
        
        if time.time() - start_time >= 60:
            break
    
    print("Debate time has ended.")
    
    # Display token usage
    print(f"\nEstimated total tokens used: {total_tokens}")
    
    # Calculate and display cost (assuming GPT-3.5-turbo pricing)
    cost_per_1k_tokens = 0.002  # $0.002 per 1K tokens for GPT-3.5-turbo
    estimated_cost = (total_tokens / 1000) * cost_per_1k_tokens
    print(f"Estimated cost: ${estimated_cost:.4f}")

# Get user input for the debate topic
debate_topic = input("Enter the debate topic: ")

# Run the debate
run_debate(debate_topic)
