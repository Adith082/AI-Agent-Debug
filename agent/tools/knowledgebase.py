from .base import BaseTool, ToolResult
from agent.schemas import KBArgs
import json, os
from sentence_transformers import SentenceTransformer, util
from pathlib import Path

class KnowledgeBaseTool(BaseTool):
    name = "knowledgebase"
    args_model = KBArgs
    _model = SentenceTransformer("all-MiniLM-L6-v2")

    def run(self, args: KBArgs) -> ToolResult:
        try:
            
            
           # root_dir = Path(__file__).resolve().parent.parent
           # kb_path = root_dir / "data" / "kb.json"
            
            with open("data/kb.json", "r", encoding="utf-8") as f:
                data = json.load(f)
            entries = data.get("entries", [])
            if not entries:
                return ToolResult(ok=False, error="KB empty")
            corpus = [f"{e.get('name','')} {e.get('summary','')}" for e in entries]
            corpus_emb = self._model.encode(corpus, convert_to_tensor=True)
            q_emb = self._model.encode(args.q, convert_to_tensor=True)
            scores = util.pytorch_cos_sim(q_emb, corpus_emb)[0]
            idx = scores.argmax().item()
            return ToolResult(ok=True, data=entries[idx]["summary"])
        except Exception as e:
            return ToolResult(ok=False, error=str(e))