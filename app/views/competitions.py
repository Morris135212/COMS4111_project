# -*- coding: utf-8 -*-
import datetime

from app import app
from flask import Flask, request, render_template, g, redirect, Response

from app.models import Competition, Participants, Users

COMPETITIONS = ['Titanic - Machine Learning from Disaster', 'NFL Health & Safety - Helmet Assignment']


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

    sql = "SELECT COUNT(*) FROM USERS u " \
          "WHERE u.u_id in " \
          "(SELECT u_id from Take t " \
          "WHERE t.c_name = %s);"
    cursor = g.conn.execute(sql, name).fetchone()
    context = dict(competition=competition.name,
                   start_date=competition.start_date,
                   end_date=competition.end_date,
                   prize=competition.prize,
                   rank=rank,
                   f_name=f_name,
                   l_name=l_name,
                   scores=scores,
                   num=cursor[0])
    print(context)
    return render_template("competition.html", **context)


@app.route('/sign_in', methods=['GET', 'POST'])
def sign():
    fname = request.form['fname']
    lname = request.form['lname']
    web = request.form['web']
    university = request.form['university']
    competition = request.form['comp']
    import re
    competition = list(filter(lambda x: re.compile(competition).findall(x), COMPETITIONS))[0]
    print(f"fname: {fname}, lname: {lname}, web:{web}, university: {university}, competition: {competition}")
    sql = "SELECT * FROM USERS " \
          "WHERE f_name = %s AND l_name = %s AND webpage_link = %s AND UNIVERSITY_name = %s"
    results = g.conn.execute(sql, fname, lname, web, university).fetchall()
    if results:
        user = Users(*results[0])
        try:
            insert_sql = "INSERT INTO take (score, paticipant_date, u_id, c_name) VALUES (%s, %s, %s, %s)"
            import datetime
            now_time = datetime.datetime.now().strftime('%Y-%m-%d')
            g.conn.execute(insert_sql, .0, now_time, user.u_id, competition)
        except Exception as e:
            context = dict(error="You have joined the competition")
            return render_template("500.html", **context)
        return redirect('/')
    context = dict(error="User not found in database")
    return render_template("500.html", **context)


