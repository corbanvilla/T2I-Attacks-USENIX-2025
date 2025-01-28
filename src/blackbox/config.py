import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

if "OPENAI_API_KEY" not in os.environ:
    raise ValueError("OPENAI_API_KEY is not set in the environment variables")
if "OPENAI_ORG_KEY" not in os.environ:
    raise ValueError("OPENAI_ORG_KEY is not set in the environment variables")

client = OpenAI(
    api_key=os.environ["OPENAI_API_KEY"],
    organization=os.environ["OPENAI_ORG_KEY"],
)
