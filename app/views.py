# -*- coding: utf-8 -*-
from app import app
from flask import Flask, request, render_template, g, redirect, Response

from app.models import Competition, Participants


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/competition', methods=['GET', 'POST'])
def comp():
    name = request.form['comp']
    print(f"The name of competition {name}")
    cursor = g.conn.execute('SELECT * FROM competitions WHERE name = %s', name)
    result = cursor.fetchone()
    competition = Competition(*result)
    # print(competition)
    sql = "SELECT u.f_name, u.l_name, t.score from USERS u " \
          "INNER JOIN  Take t ON u.u_id = t.u_id " \
          "WHERE t.c_name = %s " \
          "ORDER BY t.score DESC " \
          "LIMIT 10"
    cursor = g.conn.execute(sql, name).fetchall()

    rank = []
    f_name, l_name, scores = [], [], []
    for i, result in enumerate(cursor):
        participant = Participants(*result)
        rank.append(i+1)
        f_name.append(participant.f_name)
        l_name.append(participant.l_name)
        scores.append(participant.score)

    context = dict(competition=competition.name,
                   start_date=competition.start_date,
                   end_date=competition.end_date,
                   prize=competition.prize,
                   rank=rank,
                   f_name=f_name,
                   l_name=l_name,
                   scores=scores)
    print(context)
    return render_template("competition.html", **context)


