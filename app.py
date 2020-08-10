from flask import Flask, request, redirect, url_for, render_template
from flask_sqlalchemy import SQLAlchemy
import os

from methods import *
from os import environ

from methods import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DATABASE_URL') or 'sqlite:///tb1.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'dont-touch-me'
db = SQLAlchemy(app)


# TODO create error page

@app.route('/', methods=["GET", "POST"])
def welcome_page():
    if request.method == "POST":
        name = request.form['name']
        if name is None:
            print("Please enter a name")

        # creates new user and returns user_id
        user_id = create_new_user(name)
        user = User.query.get(user_id)
        sub_round = user.sub_round

        items = next_competitors_w(user_id)

        return redirect(url_for('tournament', user_id=user_id, name=name,
                                item_1=items[0], item_2=items[1]))

    return render_template('welcome.html')


@app.route('/tournament/<int:user_id>-<name>/<item_1>-<item_2>', methods=["GET", "POST"])
def tournament(user_id, name, item_1, item_2):
    user = User.query.get(user_id)
    name = user.username
    if request.method == "POST":
        user_pick = request.form['items']
        if user.sub_round < 7:
            if user_pick == 'one':
                round_one_winner(user_id, item_1, item_2)
            elif user_pick == 'two':
                round_one_winner(user_id, item_2, item_1)
            else:
                print("error")
            items = next_competitors_w(user_id)
            increase_subround(user_id)
            return redirect(url_for('tournament', user_id=user.id, sub_round=user.sub_round,
                                    name=name, item_1=items[0], item_2=items[1]))
        elif user.sub_round < 12:
            if user_pick == 'one':
                round_two_winner(user_id, item_1)
            elif user_pick == 'two':
                round_two_winner(user_id, item_2)
            else:
                print("error")

            if user.sub_round == 11:
                items = next_competitors_l(user_id)
                print(items)
                increase_subround(user_id)
            else:
                items = next_competitors_w(user_id)
                increase_subround(user_id)
            return redirect(url_for('tournament', user_id=user.id, sub_round=user.sub_round,
                                    name=name, item_1=items[0], item_2=items[1]))
        elif user.sub_round < 17:
            if user_pick == 'one':
                round_three_winner(user_id, item_1)
            elif user_pick == 'two':
                round_three_winner(user_id, item_2)
            else:
                print("error")

            if user.sub_round != 16:
                items = next_competitors_l(user_id)
                increase_subround(user_id)
            else:
                items = final_competitors(user_id)
                print(items)
                increase_subround(user_id)
            return redirect(url_for('tournament', user_id=user.id, sub_round=user.sub_round,
                                    name=name, item_1=items[0], item_2=items[1]))

        elif user.sub_round == 17:
            if user_pick == 'one':
                final_winner(user_id, item_1)
            elif user_pick == 'two':
                final_winner(user_id, item_2)
            else:
                print("error")
            return redirect(url_for('final_list', user_id=user_id))

    return render_template("tournament.html", sub_round=user.sub_round,
                           name=name, item_1=item_1, item_2=item_2)


@app.route('/final_list/<int:user_id>')
def final_list(user_id):
    final_list = generate_final_list(user_id)
    return render_template("final_list.html", final_list=final_list)


if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
