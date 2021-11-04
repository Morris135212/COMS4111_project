from flask import request, render_template, g, redirect

from app import app
from app.models import DataSets, Tasks, Users
import numpy as np

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


@app.route("/operation", methods=["POST", "GET"])
def operation():
    op = request.form["operation"]
    fname = request.form["fname"]
    lname = request.form["lname"]
    dname = request.form["dname"]
    provenance = request.form["provenance"]
    print(f"fname:{fname}, lname:{lname}, dname:{dname}")
    if op == "Contribute":
        sql = "SELECT * FROM USERS " \
              "WHERE f_name = %s AND l_name = %s"
        results = g.conn.execute(sql, fname, lname).fetchall()
        print(results)
        try:
            assert results, "You are not in database"
            user = Users(*results[0])
            try:
                query_sql = "SELECT * FROM datasets WHERE name = %s AND provenance = %s"
                results = g.conn.execute(query_sql, dname, provenance).fetchall()
                assert not results, "You have contribute to this dataset before"

                import uuid, datetime
                idx = ''.join(np.random.choice(list(str(uuid.uuid1())), 20))
                insert_sql1 = "INSERT INTO datasets (name, idx, provenance) VALUES (%s, %s, %s)"
                g.conn.execute(insert_sql1, dname, idx, provenance)
                now_time = datetime.datetime.now().strftime('%Y-%m-%d')
                insert_sql2 = "INSERT INTO maintain (update_time, u_id, d_id) VALUES (%s, %s, %s)"
                g.conn.execute(insert_sql2, now_time, user.u_id, idx)
                context = dict(message="You have successfully add a new dataset!")
            except Exception as e:
                context = dict(error=e)
                return render_template("500.html", **context)
            return render_template('success.html', **context)
        except Exception as e:
            print(e)
            context = dict(error=e)
            return render_template("500.html", **context)