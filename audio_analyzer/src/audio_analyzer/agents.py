from crewai import Agent

class MyAgents():
    # Define the agents
    def call_analysis_agent(self, model):
        return Agent(
            role="AI-Powered Call Analyzer",
            goal="Provide actionable insights and advanced performance analysis from sales call transcriptions, empowering agents to close deals more effectively.",
            backstory="The AI-Powered Call Analyzer evaluates sales conversations by using sentiment analysis, identifying pain points, and providing detailed recommendations for improved outcomes.",
            verbose=True,
            allow_delegation=False,
            llm=model
        )