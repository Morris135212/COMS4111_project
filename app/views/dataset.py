from flask import request, render_template, g, redirect

from app import app
from app.models import DataSets, Tasks, Users, UserCodes
import numpy as np

COMPTITIONS = ['Titanic - Machine Learning from Disaster', 'NFL Health & Safety - Helmet Assignment']


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
    query = "SELECT t.t_id, t.name, t.description, t.d_id " \
            "FROM datasets d " \
            "INNER JOIN tasks t ON d.idx = t.d_id " \
            "WHERE d.idx = %s"
    results = g.conn.execute(query, idx).fetchall()
    tasks = []
    for i, result in enumerate(results):
        task = Tasks(*result)
        print(task)
        tasks.append(task.__dict__)
    context = dict(tasks=tasks, dataset=data)
    print(f"{context}, idx: {idx}")
    return render_template("tasks.html", **context)


@app.route("/task", methods=["POST", "GET"])
def tasks():
    t_id = request.form["t_id"]
    query1 = "SELECT * FROM tasks WHERE t_id = %s"
    result = g.conn.execute(query1, t_id).fetchall()[0]
    task = Tasks(*result)
    task = task.__dict__

    d_id = request.form["d_id"]
    query2 = "SELECT * FROM datasets WHERE idx = %s"
    result = g.conn.execute(query2, d_id).fetchall()[0]
    dataset = DataSets(*result)
    dataset = dataset.__dict__

    query3 = "SELECT u.f_name, u.l_name, c.code, c.stars, c.output_file " \
             "from USERS u " \
             "INNER JOIN Codes c ON " \
             "u.u_id = c.u_id " \
             "WHERE c.t_id = %s " \
             "ORDER BY c.stars " \
             "DESC LIMIT 10;"
    results = g.conn.execute(query3, t_id).fetchall()
    rank, usercodes = [], []
    for i, result in enumerate(results):
        rank.append(i + 1)
        usercode = UserCodes(*result)
        usercodes.append(usercode.__dict__)
    context = dict(task=task, dataset=dataset, usercodes=usercodes, rank=rank)
    return render_template("task.html", **context)


@app.route("/submit_task", methods=["POST", "GET"])
def submit_task():
    t_id = request.form["t_id"]
    query = "SELECT * FROM tasks WHERE t_id = %s"
    result = g.conn.execute(query, t_id).fetchall()[0]
    task = Tasks(*result)
    context = dict(task=task)
    return render_template("submit.html", **context)


@app.route("/submit_code", methods=["POST", "GET"])
def submit_code():
    fname = request.form["fname"]
    lname = request.form["lname"]
    code = request.form["code"]
    t_id = request.form["t_id"]
    out_file = request.form["output"]
    print(f"fname: {fname}, lname:{lname}, code:{code}, out_file: {out_file}, t_id: {t_id}")
    sql = "SELECT * FROM USERS " \
          "WHERE f_name = %s AND l_name = %s"
    results = g.conn.execute(sql, fname, lname).fetchall()
    try:
        assert results, "You are not in database"
        user = Users(*results[0])
        try:
            query_sql = "SELECT * FROM codes WHERE code = %s"
            results = g.conn.execute(query_sql, code).fetchall()
            print(results)
            assert not results, "The results has been repeated submitted"
            import uuid, datetime
            idx = ''.join(np.random.choice(list(str(uuid.uuid1())), 20))
            now_time = datetime.datetime.now().strftime('%Y-%m-%d')
            params = [idx, code, now_time, t_id, user.u_id]
            if out_file != '':
                insert_sql = "INSERT INTO codes (idx, code, submit_date, t_id, u_id, output_file) " \
                             "VALUES (%s, %s, %s, %s, %s, %s)"
                params.append(out_file)
            else:
                insert_sql = "INSERT INTO codes (idx, code, submit_date, t_id, u_id) " \
                             "VALUES (%s, %s, %s, %s, %s)"
            g.conn.execute(insert_sql, *params)
        except Exception as e:
            print(e)
            context = dict(error=e)
            return render_template("500.html", **context)
    except Exception as e:
        print(e)
        context = dict(error=e)
        return render_template("500.html", **context)
    context = dict(message="You successfully submit the code!")
    return render_template("success.html", **context)


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


@app.route("/update_request", methods=["POST", "GET"])
def update_request():
    context = dict(operation="Update")
    return render_template("update.html", **context)


@app.route("/update", methods=["POST", "GET"])
def update():
    op = request.form["operation"]
    u_id = request.form["u_id"]
    d_id = request.form["d_id"]
    print(f"u_id:{u_id}, d_id:{d_id}")
    if op == "Update":
        sql = "SELECT * FROM maintain " \
              "WHERE u_id = %s AND d_id = %s"
        results = g.conn.execute(sql, u_id, d_id).fetchall()
        print(results)
        try:
            assert results, "This user or this dataset does not exist!"
            insert_sql = "INSERT maintain (update_time, u_id, d_id) VALUES (%s, %s, %s)" \
                         "WHERE u_id = %s AND d_id = %s"
            import datetime
            now_time = datetime.datetime.now().strftime('%Y-%m-%d')
            g.conn.execute(insert_sql, now_time, u_id, d_id, u_id, d_id)
            context = dict(message="You have successfully add a new dataset!")
            return render_template('success.html', **context)
        except Exception as e:
            print(e)
            context = dict(error=e)
            return render_template("500.html", **context)
