from textwrap import dedent
from dotenv import load_dotenv

from agno.team.team import Team

from model_config import build_model

from youtube_agent import build_youtube_agent
from fact_check_agent import build_fact_check_agent
from memory import db

load_dotenv(override=True)

def build_supervisor_agent():

    youtube_agent = build_youtube_agent()
    fact_check_agent = build_fact_check_agent()

    return Team(
        name="Multi-Agent AI",
        model=build_model("supervisor", max_tokens=700),

        members=[
            youtube_agent,
            fact_check_agent
        ],

        db=db,
        max_iterations=4,
        tool_call_limit=6,
        compress_tool_results=True,
        store_history_messages=True,
        add_history_to_context=True,
        num_history_runs=3,
        read_chat_history=True,
        add_team_history_to_members=True,

        instructions=dedent("""\
            You are the supervisor of a multi-agent YouTube analysis system.

            Your job is to coordinate the YouTube Agent and Fact Check Agent.

            Workflow:
                1. Ask the YouTube Agent to analyze the YouTube video.
                2. For a normal video URL, return one concise final analysis.
                3. The final analysis must include these exact headings:
                    ## Video Overview
                    ## Summary
                    ## Main Points
                    ## Notable Factual Claims
                4. Under Notable Factual Claims, list 3 to 5 claims from the video.
                5. Use the Fact Check Agent only when the user explicitly asks to
                    fact-check or verify claims. Limit verification to 3 claims.
                6. For follow-up questions, use the previous video and chat history.
                    Never ask the user to provide the URL again when it is already
                    present in the current session.
        """),

        markdown=True,
    )