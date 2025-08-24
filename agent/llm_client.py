from openai import OpenAI
import os

client = OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key= os.getenv("OPENAI_API_KEY") ,
)

def combine_with_llm(prompt: str) -> str:
    system = ("You are a helpful assistant. The user will provide a question and "
    "some tool-generated results. Provide the final answer with a brief "
    "do NOT include any explanations or extra text.")
    c = client.chat.completions.create(
        model="openai/gpt-oss-20b:free",
        messages=[{"role":"system","content":system},{"role":"user","content":prompt}],
        temperature=0
    )
    return c.choices[0].message.content.strip()