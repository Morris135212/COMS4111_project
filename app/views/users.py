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


@app.route("/followers", methods=["POST", "GET"])
def followers():
    u_id = request.form["u_id"]
    sql = "SELECT * FROM users WHERE u_id = %s"
    user = g.conn.execute(sql, u_id).fetchall()[0]
    user = Users(*user)
    followed_query = "SELECT u.u_id, u.f_name, u.l_name, u.webpage_link, u.gold_medal, " \
                     "u.silver_medal, u.bronze_medal, u.university_name " \
                     "FROM follow f JOIN users u ON f.follower_id = u.u_id " \
                     "WHERE f.followed_id = %s"
    results = g.conn.execute(followed_query, u_id).fetchall()
    followers = []
    for i, result in enumerate(results):
        follower = Users(*result)
        followers.append(follower.__dict__)
    context = dict(users=followers, USER=user.f_name+' '+user.l_name)
    print(f"{context}, 页面主人: {u_id}")
    return render_template("users.html", **context)
