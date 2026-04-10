from flask import Flask, render_template, request

app = Flask("lovely_calculator")

@app.route("/", methods=["GET", "POST"])
def home():
    result = None

    if request.method == "POST":
        num1 = float(request.form["num1"])
        num2 = float(request.form["num2"])
        op = request.form["operation"]

        if op == "+":
            result = num1 + num2
        elif op == "-":
            result = num1 - num2
        elif op == "*":
            result = num1 * num2
        elif op == "/":
            result = num1 / num2
        elif op == "%":
            result = num1 % num2
        elif op == "**":
            result = num1 ** num2
        elif op == "//":
            result = num1 // num2
        else:
            result = "Invalid operation"

    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)
