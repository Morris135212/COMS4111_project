class Competition:
    def __init__(self, name, start_date, end_date, prize):
        self.name = name
        self.start_date = str(start_date)
        self.end_date = str(end_date)
        self.prize = prize

    def __str__(self):
        return f"competition: {self.name}, " \
               f"start from: {self.start_date}, " \
               f"end at: {self.end_date} with prize: {self.prize}"


class DataSet:
    def __init__(self, idx, name, provenance):
        self.idx = idx
        self.name = name
        self.provenance = provenance


class Users:
    def __init__(self, u_id, university_name, f_name,
                 l_name, webpage_link,
                 gold_medal=0, silver_medal=0, bronze_medal=0):
        self.u_id = u_id
        self.university_name = university_name
        self.f_name = f_name
        self.l_name = l_name
        self.webpage_link = webpage_link
        self.gold_medal = gold_medal
        self.silver_medal = silver_medal
        self.bronze_medal = bronze_medal


class Participants:
    def __init__(self, f_name, l_name, score):
        self.f_name = f_name
        self.l_name = l_name
        self.score = score


class Codes:
    def __init__(self, idx, t_id, u_id, code, output_file, submit_date, stars):
        self.idx = idx
        self.t_id = t_id
        self.u_id = u_id
        self.code = code
        self.output_file = output_file
        self.submit_date = submit_date
        self.stars = stars


class Tasks:
    def __init__(self, t_id, d_id, name, description):
        self.t_id = t_id
        self.d_id = d_id
        self.name = name
        self.description = description


class University:
    def __init__(self, name, location):
        self.name = name
        self.location = location


class Course:
    def __int__(self, idx, name, description):
        self.idx = idx
        self.name = name
        self.description = description
