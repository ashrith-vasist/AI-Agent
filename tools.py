import random

from livekit.agents import llm, function_tool, RunContext
from DSAquestions import QUESTION_BANK, DSAQuestion
import json


DSA_VALIDATION_PROMPT = f"""
You are a senior technical interviewer evaluating a candidate's DSA explanation.

Evaluation rules:
- Judge correctness strictly based on the underlying algorithmic logic.
- Ignore syntax, programming language, or minor implementation details.
- Partial or vague explanations must be marked as incorrect.
- Be strict but fair.
- Do NOT reveal chain-of-thought or internal reasoning.
- Respond ONLY in valid JSON.

Expected Logic:
{{expected_logic}}

Candidate Answer:
{{user_answer}}

Return JSON in the following format:
{{
  "is_correct": true or false,
  "feedback": "A short, clear explanation of why the answer is correct or incorrect",
  "pro_tip": "A concise optimization or insight if correct, otherwise null"
}}
"""



@function_tool(name="fetch_dsa_question")
async def fetch_dsa_question(
    phase: str,
    topic: str | None = None,
) -> dict:
    """Fetch a Random DSA question"""

    if phase == "interviewer_choice":
        topic = random.choice(list(QUESTION_BANK.keys()))

    if topic not in QUESTION_BANK:
        return {"error": "Invalid topic"}

    q: DSAQuestion = random.choice(QUESTION_BANK[topic])
    return {
        "topic": q.topic,
        "question": q.question,
        "logic": q.logic,
    }


@function_tool(name="validate_dsa_answer")
async def validate_dsa_answer(
        ctx: RunContext,
        user_answer: str,
        expected_logic: str,
)-> dict:
    """
    Validate a DSA answer using LLM reasoning.
    """

    result = await ctx.llm.chat(
        message=[
            {"role": "system", "content": DSA_VALIDATION_PROMPT},
            {
                "role": "user",
                "content": f"""
                            Candidate answer:
                            {user_answer}
                            
                            Expected logic:
                            {expected_logic}
                            """
            },
        ],
        response_format="json",  # forces structured output
    )

    return {
        "is_correct": result["is_correct"],
        "feedback": result["feedback"],
        "pro_tip": result.get("pro_tip"),
    }


@function_tool(name="give_hint")
async def give_hint(expected_logic: str) -> str:
    """
    Provide a partial hint (not full solution).
    """
    return f"Hint: Think about this idea → {expected_logic.split(',')[0]}"


