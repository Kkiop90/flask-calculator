from flask import Flask, render_template, request
import ast
import operator as op

app = Flask(__name__)

ALLOWED_OPERATORS = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.Mod: op.mod,
    ast.Pow: op.pow,
    ast.FloorDiv: op.floordiv,
    ast.UAdd: lambda x: x,
    ast.USub: op.neg,
}


def safe_eval(expression: str):
    node = ast.parse(expression, mode="eval")
    return evaluate_node(node.body)


def evaluate_node(node):
    if isinstance(node, ast.BinOp):
        left = evaluate_node(node.left)
        right = evaluate_node(node.right)
        operator_type = type(node.op)
        if operator_type in ALLOWED_OPERATORS:
            return ALLOWED_OPERATORS[operator_type](left, right)
        raise ValueError("Unsupported operator")

    if isinstance(node, ast.UnaryOp):
        operand = evaluate_node(node.operand)
        operator_type = type(node.op)
        if operator_type in ALLOWED_OPERATORS:
            return ALLOWED_OPERATORS[operator_type](operand)
        raise ValueError("Unsupported unary operator")

    if isinstance(node, ast.Constant):
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError("Invalid value")

    if isinstance(node, ast.Expr):
        return evaluate_node(node.value)

    raise ValueError("Invalid expression")


@app.route("/", methods=["GET", "POST"])
def home():
    result = None
    error = None
    expression = request.form.get("expression", "")

    if request.method == "POST":
        if request.form.get("clear"):
            expression = ""
        else:
            try:
                if not expression.strip():
                    raise ValueError("Enter an expression first.")

                result = safe_eval(expression)
            except ZeroDivisionError:
                error = "Cannot divide by zero."
            except (SyntaxError, ValueError):
                error = "Please enter a valid expression."

    return render_template(
        "index.html",
        expression=expression,
        result=result,
        error=error,
    )


if __name__ == "__main__":
    app.run(debug=True)
