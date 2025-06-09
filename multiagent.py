import subprocess
import re

class ChatCompletionAgent:
    def __init__(self, name, instructions, kernel):
        self.name = name
        self.instructions = instructions
        self.kernel = kernel

class ApprovalTerminationStrategy:
    def should_agent_terminate(self, chat_history):
        return any("APPROVED" in message['content'] for message in chat_history if message['role'] == 'user')

class AgentGroupChat:
    def __init__(self, agents, termination_strategy):
        self.agents = agents
        self.termination_strategy = termination_strategy
        self.chat_history = []

    def add_message(self, role, content):
        self.chat_history.append({'role': role, 'content': content})
        if self.termination_strategy.should_agent_terminate(self.chat_history):
            self.terminate_chat()

    def terminate_chat(self):
        html_code = self.extract_html_code()
        if html_code:
            with open("index.html", "w") as file:
                file.write(html_code)
            subprocess.run(["bash", "push_to_github.sh"])

    def extract_html_code(self):
        pattern = r"```html\\s*(.*?)```"
        for message in self.chat_history:
            if message['role'] == 'SoftwareEngineer':
                match = re.search(pattern, message['content'], re.DOTALL)
                if match:
                    return match.group(1)
        return ""

# Example usage
kernel = None  # Replace with actual kernel if needed
agents = [
    ChatCompletionAgent("BusinessAnalyst", "You are a Business Analyst...", kernel),
    ChatCompletionAgent("SoftwareEngineer", "You are a Software Engineer...", kernel),
    ChatCompletionAgent("ProductOwner", "You are a Product Owner...", kernel)
]

termination_strategy = ApprovalTerminationStrategy()
group_chat = AgentGroupChat(agents, termination_strategy)

# Simulated chat
group_chat.add_message("user", "Please build a login page.")
group_chat.add_message("SoftwareEngineer", "```html\n<html><body>Login Page</body></html>\n```")
group_chat.add_message("user", "APPROVED")
