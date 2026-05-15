import os
import json
from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage, SystemMessage
from vector_store import find_relevant_emojis

load_dotenv()

llm = ChatAnthropic(
    model="claude-sonnet-4-6",
    temperature=0.7,
    api_key=os.getenv("ANTHROPIC_API_KEY")
)


def detect_emojis(text: str, safe_search: bool = True) -> dict:
    # Step 1 — RAG: find candidate emojis from the vector database
    candidates = find_relevant_emojis(text, safe_search=safe_search)

    if not candidates:
        return {"emojis": [], "explanation": "No matching emojis found for this text."}

    emoji_list = "\n".join([f"- {e['emoji']} ({e['name']})" for e in candidates])

    # Step 2 — Build the prompt for Claude
    safe_instruction = (
        "This is a family-friendly request. Only suggest safe-for-all-ages emojis."
        if safe_search else
        "Adult content is permitted. You may include suggestive or mature emojis if relevant to the text."
    )

    system_prompt = f"""You are an expert emoji analyst. Read the user's text and suggest
the most fitting emojis from the list provided.

{safe_instruction}

You MUST respond with valid JSON only — no extra text, no markdown, no code blocks.
Use exactly this format:
{{"emojis": ["emoji1", "emoji2", "emoji3"], "explanation": "One sentence explaining why these fit."}}"""

    user_prompt = f"""Text: "{text}"

Choose the 3 to 5 most fitting emojis from this list only:
{emoji_list}

Reply with JSON only."""

    # Step 3 — Call Claude API
    response = llm.invoke([
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_prompt)
    ])

    # Step 4 — Parse the JSON response
    raw = response.content.strip()

    # Strip markdown code fences if Claude wraps the JSON
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
        raw = raw.strip()

    try:
        result = json.loads(raw)
        return result
    except json.JSONDecodeError:
        # Fallback: return top 3 candidates if JSON parsing fails
        return {
            "emojis": [e["emoji"] for e in candidates[:3]],
            "explanation": "Here are the closest matching emojis for your text."
        }
