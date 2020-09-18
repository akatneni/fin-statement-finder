from flask import Flask, render_template, request
from app.scrape import getTable

app = Flask(__name__)

# TODO: Remove Go button and replace with statement buttons
#           Put everything in 1 form, reduce redundancy
@app.route('/')
def search():
    # SEC records different names for statements
    dict = {"IS":["CONSOLIDATED STATEMENTS OF INCOME","CONSOLIDATED STATEMENTS OF OPERATIONS"],
        "BS":["CONSOLIDATED BALANCE SHEETS"],
        "CFS":["CONSOLIDATED STATEMENTS OF CASH FLOWS"]}
    CIK=request.args.get("CIK")
    statement=request.args.get("statement")
    if CIK==None or CIK=="":
        return render_template("index.html")
    table=getTable(CIK,dict[statement])
    return render_template("statements.html",CIK=CIK,table=table)
