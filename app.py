from src.criminalNetwork.config.configuration import ConfigurationManager
from src.criminalNetwork.components.agent import CriminalNetworkAgent

config = ConfigurationManager().get_agent_config()
agent = CriminalNetworkAgent(config=config)

answer = agent.answer_query(
    user_query="Who is priya's mobile number and give me all details about it",
    entity_focus="Priya Sharma"
)
print(answer, flush=True)