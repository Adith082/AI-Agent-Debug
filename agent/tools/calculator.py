# from .base import BaseTool, ToolResult
# from agent.schemas import CalculatorArgs
# import ast, operator as op

# class CalculatorTool(BaseTool):
#     name = "calculator"
#     args_model = CalculatorArgs

#     _ops = {ast.Add: op.add, ast.Sub: op.sub, ast.Mult: op.mul, ast.Div: op.truediv,
#             ast.Pow: op.pow, ast.USub: op.neg, ast.Mod: op.mod, ast.FloorDiv: op.floordiv}

#     def _eval(self, node):
#         if isinstance(node, ast.Num): return node.n
#         if isinstance(node, ast.BinOp): return self._ops[type(node.op)](self._eval(node.left), self._eval(node.right))
#         if isinstance(node, ast.UnaryOp): return self._ops[type(node.op)](self._eval(node.operand))
#         raise TypeError(f"Unsupported: {node}")

#     def run(self, args: CalculatorArgs) -> ToolResult:
#         try:
#             node = ast.parse(args.expr.strip(), mode="eval").body
#             return ToolResult(ok=True, data=self._eval(node))
#         except Exception as e:
#             return ToolResult(ok=False, error=str(e))


from .base import BaseTool, ToolResult
from agent.schemas import CalculatorArgs
import ast, operator as op
import re

class CalculatorTool(BaseTool):
    name = "calculator"
    args_model = CalculatorArgs

    _ops = {
        ast.Add: op.add,
        ast.Sub: op.sub,
        ast.Mult: op.mul,
        ast.Div: op.truediv,
        ast.Pow: op.pow,
        ast.USub: op.neg,
        ast.Mod: op.mod,
        ast.FloorDiv: op.floordiv,
    }

    def _eval(self, node):
        if isinstance(node, ast.Constant):  # Python 3.8+ uses Constant
            return node.value
        elif isinstance(node, ast.Num):  # For backward compatibility
            return node.n
        elif isinstance(node, ast.BinOp):
            return self._ops[type(node.op)](self._eval(node.left), self._eval(node.right))
        elif isinstance(node, ast.UnaryOp):
            return self._ops[type(node.op)](self._eval(node.operand))
        else:
            raise TypeError(f"Unsupported type: {node}")

    def _preprocess(self, expr: str) -> str:
        """
        Convert natural language percentages to Python expressions.
        e.g., "12.5% of 243" -> "(12.5/100)*243"
        """
        expr = expr.lower().replace("what is", "").strip()
        # Replace patterns like "X% of Y"
        match = re.search(r'([\d.]+)\s*%\s*of\s*([\d.]+)', expr)
        if match:
            x, y = match.groups()
            expr = expr.replace(match.group(0), f"({x}/100)*{y}")
        return expr

    def run(self, args: CalculatorArgs) -> ToolResult:
        try:
            expr = self._preprocess(args.expr.strip())
            node = ast.parse(expr, mode="eval").body
            return ToolResult(ok=True, data=self._eval(node))
        except Exception as e:
            return ToolResult(ok=False, error=str(e))
