from app import app
from flask import Flask, request, render_template, g, redirect, Response

from app.models import DataSets, Tasks

COMPETITIONS = ['Titanic - Machine Learning from Disaster', 'NFL Health & Safety - Helmet Assignment']


@app.route("/dataset")
def dataset():
    sql = "SELECT * FROM datasets"
    results = g.conn.execute(sql).fetchall()
    datasets = []
    for i, result in enumerate(results):
        data = DataSets(*result)
        datasets.append(data.__dict__)
    context = dict(datasets=datasets)
    print(context)
    return render_template("dataset.html", **context)


@app.route("/dataset_detail", methods=["POST", "GET"])
def detail():
    idx = request.form["dataset_idx"]
    sql = "SELECT * FROM datasets WHERE idx = %s"
    data = g.conn.execute(sql, idx).fetchall()[0]
    data = DataSets(*data)
    query = "SELECT t.t_id, t.d_id, t.name, t.description " \
            "FROM datasets d " \
            "INNER JOIN tasks t ON d.idx = t.d_id " \
            "WHERE d.idx = %s"
    results = g.conn.execute(query, idx).fetchall()
    tasks = []
    for i, result in enumerate(results):
        task = Tasks(*result)
        tasks.append(task.__dict__)
    context = dict(tasks=tasks, dataset=data.name)
    print(f"{context}, idx: {idx}")
    return render_template("tasks.html", **context)


@app.route("/contribute", methods=["POST", "GET"])
def contribute():
    context = dict(operation="Contribute")
    return render_template("contribute.html", **context)