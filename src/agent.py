"""OpenShell Deep Agent.

General-purpose coding and analysis agent using OpenShell as the on-prem
sandbox provider. Executes code inside a policy-governed OpenShell sandbox
with local filesystem persistence for memory and skills.

Quick start:
  1. Start or select a gateway: openshell gateway start
  2. (Optional) Pre-create a sandbox: openshell sandbox create --name my-sandbox --keep
     Then set: export OPENSHELL_SANDBOX_NAME=my-sandbox
  3. Run: deepagents run src/agent.py:agent
"""

import os
from datetime import datetime

from deepagents import create_deep_agent
from langchain.chat_models import init_chat_model
from langchain_nvidia_ai_endpoints import ChatNVIDIA

from src.backend import create_backend
from src.prompts import AGENT_INSTRUCTIONS

current_date = datetime.now().strftime("%Y-%m-%d")

# Default: NVIDIA Nemotron Super 3 via NIM (ChatNVIDIA).
# Alternate: set AGENT_MODEL to a provider:model string for init_chat_model
# (e.g. anthropic:claude-sonnet-4-6 with ANTHROPIC_API_KEY).
DEFAULT_NVIDIA_MODEL = "nvidia/nemotron-3-super-120b-a12b"


def create_model():
    """Build the chat model from env.

    Unset AGENT_MODEL (or nvidia/… / nvidia:…) → ChatNVIDIA + NVIDIA_API_KEY.
    Any other provider:model string → init_chat_model (provider package + key).
    """
    agent_model = os.getenv("AGENT_MODEL", "").strip() or DEFAULT_NVIDIA_MODEL

    use_nvidia = agent_model == DEFAULT_NVIDIA_MODEL or agent_model.startswith(
        ("nvidia/", "nvidia:")
    )
    if use_nvidia:
        model_name = (
            agent_model.split(":", 1)[1]
            if agent_model.startswith("nvidia:")
            else agent_model
        )
        return ChatNVIDIA(
            model=model_name,
            api_key=os.getenv("NVIDIA_API_KEY"),
            temperature=0.1,
            max_tokens=16384,
        )

    return init_chat_model(agent_model)


model = create_model()

agent = create_deep_agent(
    model=model,
    system_prompt=AGENT_INSTRUCTIONS.format(date=current_date),
    memory=["/memory/AGENTS.md"],
    skills=["/skills/"],
    backend=create_backend,
)
