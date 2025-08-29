from crewai import Task
from textwrap import dedent

class MyTasks():
    def call_analysis_task(self, transcription, call_analysis_agent):
        return Task(
            description=dedent(f"""
                Analyze a sales call transcription between a customer and an agent.
                Generate a detailed and comprehensive report that includes:

                - Sentiment Analysis: Evaluate the customer's tone and mood throughout the call.
                - Key Phrases: Extract critical phrases that indicate interests, concerns, or objections.
                - Customer Pain Points: Identify specific issues or obstacles the customer expressed during the call.
                - Agent Effectiveness Score: Provide a score out of 10 evaluating the agent's performance in handling the call.
                - Sales Opportunities: Highlight any opportunities for upselling or cross-selling.
                - Competitor Mentions: Note if the customer referred to competitors and what was mentioned.
                - Call Engagement: Analyze how engaged the customer was during the conversation (e.g., level of questions asked, responsiveness, and tone).
                - Recommendations: Offer tailored advice for the agent to improve their approach in future calls.
                - Actionable Insights: Provide clear next steps for both the agent and the customer, with assigned responsibilities and timelines.

                Structure your response as a JSON object with the following keys:
                - sentiment_analysis
                - key_phrases
                - customer_pain_points
                - agent_effectiveness_score
                - sales_opportunities
                - competitor_mentions
                - call_engagement
                - recommendations
                - actionable_insights

                If any key is not relevant or no information is found, explicitly state "No relevant information found" for that key.
                The JSON must be concise, structured, and professional.

                Here is the transcription for analysis:
                {transcription}
            """),
            expected_output=dedent("""
                {
                    "sentiment_analysis": "Describe the sentiment of the customer interaction, including any notable emotional tone or reservations.",
                    "key_phrases": [
                        "List key phrases that capture the customer's main interests, concerns, or preferences."
                    ],
                    "customer_pain_points": [
                        "List specific challenges, objections, or concerns raised by the customer during the conversation."
                    ],
                    "agent_effectiveness_score": "Provide a rating or score based on the agent's performance, including aspects like communication, problem-solving, and empathy.",
                    "sales_opportunities": [
                        "Identify potential sales opportunities based on the conversation, such as upselling or cross-selling.",
                        "Include any suggestions that could drive revenue or offer value to the customer."
                    ],
                    "competitor_mentions": "Mention any competitors that were brought up by the customer and relevant context (e.g., features, pricing, service).",
                    "call_engagement": "Describe the level of customer engagement during the call, noting any periods of silence, hesitation, or active discussion.",
                    "recommendations": "Provide strategic recommendations based on the analysis of the conversation, aimed at improving the interaction or future sales success.",
                    "actionable_insights": [
                        {
                            "action": "Describe specific actions that can be taken to address the customer’s concerns or enhance the sales process.",
                            "assigned_to": "Specify the individual or team responsible for the action.",
                            "timeline": "Provide a timeframe or deadline for completing the action."
                        },
                    ]
                }
            """),
            agent=call_analysis_agent
        )