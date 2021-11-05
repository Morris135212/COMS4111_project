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


@app.route("/follower")
def followers():
    """
    Search followers for certain users
    //Who follows users – whose first name is Hiroshi and last name is Oshio?
    SELECT u1.u_id, u1.f_name, u1.l_name FROM USERS u1
    WHERE u1.u_id in (
	    SELECT f.follower_id FROM USERS u2
	    INNER JOIN
	    FOLLOW f
	    ON
	    u2.u_id = f.followed_id
	    WHERE u2.f_name = 'Hiroshi' AND u2.l_name = 'Oshio');
    """
    pass
