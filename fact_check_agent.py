from textwrap import dedent
from dotenv import load_dotenv

from agno.agent import Agent
from agno.tools.duckduckgo import DuckDuckGoTools

from model_config import build_model

load_dotenv()


def build_fact_check_agent():
    return Agent(
        name="Fact Check Agent",
        model=build_model("fact_check", max_tokens=700),
        
        tools=[DuckDuckGoTools()],
        instructions=dedent("""\
            You are an expert fact-checking agent.

            Your job is to verify important factual claims from
            YouTube video summaries.

            Follow these steps:

            1. Identify important factual claims.
            2. Search the web using DuckDuckGo.
                    Use only the available web_search tool. Do not call web_open,
                    browser tools, or any tool that is not available.
            3. Compare the claim with reliable sources.
            4. Determine whether the claim is:
               - Accurate
               - Inaccurate
               - Partially Accurate
               - Unclear
            5. Give a short explanation with the relevant evidence.

            Quality Guidelines:
            - Do not blindly trust the video.
            - Prefer reliable and authoritative sources.
            - Do not make unsupported claims.
            - Clearly mention when information cannot be verified.
        """),
        add_datetime_to_context=True,
        markdown=True,
    )