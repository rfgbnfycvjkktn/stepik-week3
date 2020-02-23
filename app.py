from flask import Flask, render_template, request
import data
import random
import json

app = Flask(__name__)

day_dict = {'mon':'Понедельник', 'tue':'Вторник','wed':'Среда','thu':'Четверг','fri':'Пятница','sat':'Суббота','sun':'Воскресенье'}

@app.route('/')
def index_r():
    teach_list = data.teachers
    random.shuffle(teach_list)
    goals_dict = data.goals
    return render_template('index.html', teachers=teach_list, goals_data=goals_dict)

@app.route('/goals/<goal>/')
def goal_r(goal):
    clear_teach = []
    for item in data.teachers:
        if goal in item['goals']:
            clear_teach.append(item)
    return render_template('goal.html', name=data.goals[goal].lower(), teachers=clear_teach)

@app.route('/profiles/<id_teacher>/')
def teach_r(id_teacher):
    teach = data.teachers[int(id_teacher)]

    # непонятен шаг с записью в файл. Типа записали и тут же прочитали, и послали в шаблон прочитанное и преобразованное в словарь?
    dumped = json.dumps(teach)
    teach_data = json.loads(dumped)

    return render_template('profile.html', id_teach=id_teacher, data_teach=teach_data,
                           data_goals=data.goals, days=day_dict)


@app.route('/booking/<id_teacher>/<b_day>/<b_time>/')
def booking_r(id_teacher, b_day, b_time):
    teacher = data.teachers[int(id_teacher)]

    return render_template('booking.html', b_day=b_day, b_time=int(b_time), data_teach=teacher, days=day_dict)

@app.route('/request/')
def req_r():
    return render_template('request.html')

@app.route('/request_done/',  methods=['POST'])
def request_parse_request():
    answer_dict = {"goal": request.form["goal"], "time": request.form["time"], "clientName": request.form["clientName"],
                   "clientPhone": request.form["clientPhone"]}

    with open("request.json", "w") as f:
        json.dump(answer_dict, f)

    return render_template('request_done.html')

@app.route('/booking_done/',  methods=['GET'])
def booking_parse_request():
    answer_dict = {'clientPhone': request.args.get('clientPhone'), 'clientWeekday': request.args.get('clientWeekday'),
                   'clientTime': request.args.get('clientTime'), 'clientName': request.args.get('clientName'),
                   'clientTeacher': request.args.get('clientTeacher')}

    with open("booking.json", "w") as f:
        json.dump(answer_dict, f)

    return render_template('booking_done.html', data_dict=answer_dict, days=day_dict)

if __name__ == '__main__':
    app.run()