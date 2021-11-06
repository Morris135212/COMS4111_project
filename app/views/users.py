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
    context = dict(users=followers, USER=user.f_name + ' ' + user.l_name)
    print(f"{context}, 页面主人: {u_id}")
    return render_template("users.html", **context)


@app.route("/register", methods=["POST", "GET"])
def register():
    context = dict(operation="Register")
    return render_template("register.html", **context)


@app.route("/user_register", methods=["POST", "GET"])
def user_register():
    op = request.form["operation"]
    fname = request.form["fname"]
    lname = request.form["lname"]
    u_id = request.form["u_id"]
    university = request.form["university"]
    agree = request.form["agreement"]
    print(f"fname:{fname}, lname:{lname}, u_id:{u_id}, agree:{agree}")
    if op == "Register":
        sql = "SELECT * FROM USERS " \
              "WHERE u_id = %s"
        results = g.conn.execute(sql, u_id).fetchall()
        print(results)
        try:
            assert agree == "Yes", "You did not agree to the Terms of Service!"
            try:
                assert not results, "You have already registered!"
                insert_sql = "INSERT INTO users (u_id, f_name, l_name, webpage_link, gold_medal, " \
                             "silver_medal, bronze_medal, UNIVERSITY_name) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
                g.conn.execute(insert_sql, u_id, fname, lname, 'www.kaggle.com/' + u_id, 0, 0, 0, university)
                context = dict(message="You have successfully registered!")
                return render_template('success.html', **context)
            except Exception as e:
                context = dict(error=e)
                return render_template("500.html", **context)
        except Exception as e:
            context = dict(error=e)
            return render_template("500.html", **context)
