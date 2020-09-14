from flask import Flask, render_template, request
from app.scrape import getTable

app = Flask(__name__)

@app.route('/')
def search():
    return render_template("index.html")


# balanceSheet="4"
# incomeStatement="2"
# cashFlowStatement="7"
@app.route('/statements', methods=["POST"])
def statements():
    dict = {"income":"2","balance":"4","cash":"7"}
    CIK=request.form.get("CIK")
    statement=request.form.get("statement")
    print(CIK)
    table=""
    if CIK==None:
        if statement=="Income Statement":
            table=getTable("",dict["income"])
        elif statement=="Cash Flow Statement":
            table=getTable("",dict["cash"])
        elif statement=="Balance Sheet":
            table=getTable("",dict["balance"])
    else:
        table = getTable(CIK,dict["income"])
    return render_template("statements.html",table=table)
