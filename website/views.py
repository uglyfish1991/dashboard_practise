from flask import Blueprint, render_template, request, redirect, url_for, send_file, Response
from .models import Salesfigures
from . import db
import pandas as pd
import openpyxl
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

import os


my_view = Blueprint("my_view", __name__)

@my_view.route("/")
def home():
    salesfigures_list = Salesfigures.query.all()
    return render_template("index.html", salesfigures_list=salesfigures_list)


@my_view.route("/add", methods=["POST"])
def add():
    drinks_sold = request.form.get("drinks_sold", type=int)
    money_made = request.form.get("money_made", type = int)
    new_salesfigures = Salesfigures(drinks_sold = drinks_sold, money_made = money_made, mean = (money_made/drinks_sold))
    db.session.add(new_salesfigures)
    db.session.commit()
    return redirect(url_for("my_view.home"))

@my_view.route("/generate")
def generate():
    results = Salesfigures.query.all()
    df = pd.DataFrame([(r.id, r.drinks_sold, r.money_made, r.mean) for r in results], columns=['id', 'Sold', 'Profit', "Mean"])
    print(df)
    df.to_excel("sales_figures.xlsx", sheet_name = 'Sales Figures', index = False)
    
    return send_file('../sales_figures.xlsx')

def graph_generate():
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    means = Salesfigures.query.filter(Salesfigures.mean).limit(7).all()
    means = [(mean.mean) for mean in means]
    print(means)

    plt.scatter(days, means)
    plt.xlabel("Day of the Week")
    plt.ylabel("Mean Price of Drink")

    return plt

@my_view.get("/see_graph")
def see_graph():
    plot = graph_generate()

    plot.savefig('website/static/images/plot.png')

    return render_template("plot1.html")


