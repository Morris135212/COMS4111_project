from app import app
from flask import Flask, request, render_template, g, redirect, Response

from app.models import Users


@app.route("/users")
def users():
    sql = "SELECT * FROM users"
    results = g.conn.execute(sql).fetchall()
    users = []
    for i, result in enumerate(results):
        user = Users(*result)
        users.append(user.__dict__)
    context = dict(users=users, USER="USER")
    print(context)
    return render_template("users.html", **context)
