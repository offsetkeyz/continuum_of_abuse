from app import *
import random


# adds terms to the database
def add_terms():
    t1 = Term(id=1, term='Jealousy', description='')
    t2 = Term(id=2, term='Yelling', description='')
    t3 = Term(id=3, term='Silent Treatment', description='')
    t4 = Term(id=4, term='Isolation', description='')
    t5 = Term(id=5, term='Humiliation', description='')
    t6 = Term(id=6, term='Death Threat', description='')
    t7 = Term(id=7, term='Suicide Threat', description='')
    t8 = Term(id=8, term='Choking or Strangulation', description='')
    t9 = Term(id=9, term='Pushing', description='')
    t10 = Term(id=10, term='Cheating', description='')
    t11 = Term(id=11, term='Explosive Anger', description='')
    t12 = Term(id=12, term='Constant Criticism', description='')

    db.session.add(t1)
    db.session.add(t2)
    db.session.add(t3)
    db.session.add(t4)
    db.session.add(t5)
    db.session.add(t6)
    db.session.add(t7)
    db.session.add(t8)
    db.session.add(t9)
    db.session.add(t10)
    db.session.add(t11)
    db.session.add(t12)

    db.session.commit()


# creates a new user
def create_new_user(user_name):
    term_list = Term.query.all()
    if len(term_list) == 0:
        add_terms()
        term_list = Term.query.all()

    # random.shuffle(term_list)
    winners_list = ""
    winners_v = 'fffffffffffffffffftffff'
    losers_v = 'fffffftffff'

    for term in term_list:
        winners_list = winners_list + str(term.id) + " - "

    user = User(username=user_name, sub_round=1, winners_list=winners_list,
                winners_visited=winners_v, losers_visited=losers_v)
    db.session.add(user)
    db.session.commit()

    return user.id


def increase_subround(user_id):
    user = User.query.get(user_id)
    user.sub_round = user.sub_round + 1
    db.session.commit()


# provides the next competitors from the winners bracket
def next_competitors_w(user_id):
    user = User.query.get(user_id)
    winners_list = user.winners_list
    winners_list = winners_list.split(' - ')
    if user.sub_round != 11:
        winners_visited = user.winners_visited
        winners_visited = list(winners_visited)

        first_index = winners_visited.index('f')
        winners_visited[first_index] = 't'

        second_index = winners_visited.index('f')
        winners_visited[second_index] = 't'

        separator = ""
        user.winners_visited = separator.join(winners_visited)
        try:
            db.session.commit()
        except:
            print("Failure in next_competitors_w")

        comp_1 = Term.query.get(winners_list[first_index].strip())
        comp_2 = Term.query.get(winners_list[second_index].strip())
    else:
        comp_1 = Term.query.get(winners_list[22].strip())
        comp_2 = Term.query.get(winners_list[21].strip())

    return [comp_1, comp_2]


def next_competitors_l(user_id):
    user = User.query.get(user_id)
    losers_list = user.losers_list
    losers_list = losers_list.split(' - ')

    losers_visited = user.losers_visited
    losers_visited = list(losers_visited)

    first_index = losers_visited.index('f')
    losers_visited[first_index] = 't'

    second_index = losers_visited.index('f')
    losers_visited[second_index] = 't'

    separator = ""
    user.losers_visited = separator.join(losers_visited)
    try:
        db.session.commit()
    except:
        print("Failure in next_competitors_l")

    comp_1 = Term.query.get(losers_list[first_index].strip())
    comp_2 = Term.query.get(losers_list[second_index].strip())

    return [comp_1, comp_2]


def final_competitors(user_id):
    user = User.query.get(user_id)

    losers_list = user.losers_list
    losers_list = losers_list.split(' - ')

    winners_list = user.winners_list
    winners_list = winners_list.split(' - ')

    comp_1 = Term.query.get(winners_list[-2].strip())
    comp_2 = Term.query.get(losers_list[-2].strip())
    return [comp_1, comp_2]


# sends winner to end of winners bracket
#   and loser to losers bracket
def round_one_winner(user_id, winner, loser):
    # print("winner: " + winner)
    user = User.query.get(user_id)
    winner_query = Term.query.filter(Term.term == winner)
    w_term_id = winner_query[0].id
    user.winners_list = user.winners_list + str(w_term_id) + " - "
    db.session.commit()

    loser_query = Term.query.filter(Term.term == loser)
    l_term_id = loser_query[0].id
    if user.losers_list is None:
        user.losers_list = str(l_term_id) + " - "
    else:
        user.losers_list = user.losers_list + str(l_term_id) + " - "
    db.session.commit()


def round_two_winner(user_id, winner):
    user = User.query.get(user_id)
    winner_query = Term.query.filter(Term.term == winner)
    w_term_id = winner_query[0].id
    user.winners_list = user.winners_list + str(w_term_id) + " - "
    db.session.commit()

    # TODO Make id[18] = id[21]
    winners_list = user.winners_list
    winners_list = winners_list.split(' - ')
    if len(winners_list) == 22:
        user.winners_list = user.winners_list + str(winners_list[18]) + " - "
        db.session.commit()


def round_three_winner(user_id, winner):
    user = User.query.get(user_id)
    winner_query = Term.query.filter(Term.term == winner)
    w_term_id = winner_query[0].id
    user.losers_list = user.losers_list + str(w_term_id) + " - "
    db.session.commit()

    # makes up for uneven competitors by adding wl[6] to wl[9]
    winners_list = user.losers_list
    winners_list = winners_list.split(' - ')
    if len(winners_list) == 10:
        user.losers_list = user.losers_list + str(winners_list[6]) + " - "
        db.session.commit()


def final_winner(user_id, winner):
    user = User.query.get(user_id)
    winner_query = Term.query.filter(Term.term == winner)
    w_term_id = winner_query[0].id

    user.final_winner = str(w_term_id)
    db.session.commit()


def generate_final_list(user_id):
    user = User.query.get(user_id)

    losers_list = user.losers_list
    losers_list = losers_list.split(' - ')

    winners_list = user.winners_list
    winners_list = winners_list.split(' - ')

    flist = ['none'] * 12
    # 1
    flist[0] = user.final_winner
    # 2
    w = 23
    l = 11
    for i in range(1, 12):
        print('flist: ')
        print(flist)
        if l < 0:
            i + 1
        if i % 2 == 0:
            if winners_list[w] in flist:
                while winners_list[w] in flist:
                    w = w - 1
                flist[i] = winners_list[w]
            else:
                flist[i] = winners_list[w]
        else:
            if losers_list[l] in flist:
                while losers_list[l] in flist:
                    l = l - 1
                    if l < 0:
                        i + 1
                        break
                flist[i] = losers_list[l]
            else:
                flist[i] = losers_list[l]

    for q in range(1, 13):
        print('q: ')
        print(q)
        if str(q) not in flist:
            print(str(q) + " thinks not in flist")
            flist[-1] = str(q)

    separator = " - "
    user.final_list = separator.join(flist)
    db.session.commit()

    return_list = []
    for item in flist:
        term = Term.query.filter(Term.id == item)
        return_list.append(term[0])
        print(return_list)
    return return_list


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), index=True, unique=False)
    sub_round = db.Column(db.Integer, index=False, unique=False)
    winners_list = db.Column(db.String, index=False, unique=False)
    winners_visited = db.Column(db.String, index=False, unique=False)
    losers_list = db.Column(db.String, index=False, unique=False)
    losers_visited = db.Column(db.String, index=False, unique=False)
    final_winner = db.Column(db.String, index=False, unique=False)
    final_list = db.Column(db.String, index=False, unique=False)

    # representation method
    def __repr__(self):
        return "{}".format(self.username)


# create the Song model here + add a nice representation method
class Term(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    term = db.Column(db.String(20), index=True, unique=False)
    description = db.Column(db.String(100), index=False, unique=False)

    # representation method
    def __repr__(self):
        return "{}".format(self.term)
