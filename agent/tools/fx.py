from .base import BaseTool, ToolResult
from agent.schemas import FXArgs
from agent.util.http import session_with_retries
import os

class ForeignExchangeTool(BaseTool):
    name = "foreign_currency_exchange_rate"
    args_model = FXArgs
    _http = session_with_retries()
    _api_key = os.getenv("EXCHANGERATE_API_KEY") 

    def run(self, args: FXArgs) -> ToolResult:
        if not self._api_key:
            return ToolResult(ok=False, error="Missing EXCHANGERATE_API_KEY")

        out = {}
        for base in args.bases:
            base_rates = {}
            for tgt in args.targets:
                if base == tgt:
                    base_rates[tgt] = 1.0
                    continue
                url = f"https://v6.exchangerate-api.com/v6/{self._api_key}/pair/{base}/{tgt}"
                try:
                    resp = self._http.get(url).json()
                    if resp.get("result") == "success":
                        base_rates[tgt] = resp["conversion_rate"]
                    else:
                        base_rates[tgt] = None
                except Exception:
                    base_rates[tgt] = None
            out[base] = base_rates
        return ToolResult(ok=True, data=out)