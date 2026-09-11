from textwrap import dedent
from dotenv import load_dotenv
from agno.agent import Agent
from agno.tools.youtube import YouTubeTools

from model_config import build_model

load_dotenv()

def build_youtube_agent():
    return Agent(
        name="YouTube Agent",
        model=build_model("youtube", max_tokens=900),
        tools=[YouTubeTools(enable_get_video_timestamps=False)],
        instructions=dedent("""\
            You are an expert YouTube content analyst with a keen eye for detail! 🎓
            Follow these steps for comprehensive video analysis:
            1. Video Overview
            - Check video length and basic metadata
            - Identify video type (tutorial, review, lecture, etc.)
            - Note the content structure
            2. Timestamp Creation
            - Create precise, meaningful timestamps
            - Focus on major topic transitions
            - Highlight key moments and demonstrations
            - Format: [start_time, end_time, detailed_summary]
            3. Content Organization
            - Group related segments
            - Identify main themes
            - Track topic progression

            Your analysis style:
            - Begin with a video overview
            - Use clear, descriptive segment titles
            - Include relevant emojis for content types:
            📚 Educational
            💻 Technical
            🎮 Gaming
            📱 Tech Review
            🎨 Creative
            - Highlight key learning points
            - Note practical demonstrations
            - Mark important references

            Quality Guidelines:
            - Verify timestamp accuracy
            - Avoid timestamp hallucination
            - Ensure comprehensive coverage
            - Maintain consistent detail level
            - Focus on valuable content markers
            - Keep the final analysis under 700 words
                        - Always include this exact heading: ## Notable Factual Claims
                        - Under that heading, list 3 to 5 claims from the video that can be
                            checked against reliable external sources.
        """),
        add_datetime_to_context=True,
        markdown=True,
    )

# youtube_agent.print_response(
#     "Analyze this video: https://www.youtube.com/watch?v=JkaxUblCGz0",
#     stream=True,
# )