import json
import BirdsData as Birds


def info(type_, id=0):
    data = json.load(open("balances.json", encoding="utf8"))
    lst = []
    eggs = []
    anality = {}
    for i in data['personal']:
        if i['id'] == id:
            anality = i
            break

    if type_ == "usernames":
        for i in data['personal']:
             lst.append(f"{i['username']} - {i['id']}     {i['balance']} ton     {int(info('eggs', i['id']))} eggs     {len(info('birds', i['id']))} birds")
        return lst

    elif type_ == "eggs" and id != 0:
        for egg in anality["Birds"]:
            eggs.append(egg['eggs'])
        return sum(eggs)

    elif type_ == 'balance' and id != 0:
        return anality['balance']

    elif type_ == 'birds' and id != 0:
        return anality['Birds']

    elif type_ == 'type' and id != 0:
        return anality['type']


def changeinfo(id, type_, typebird='', balance=0):
    data = json.load(open("balances.json", encoding="utf8"))

    anality = {}
    for i in data['personal']:
        if i['id'] == id:
            anality = i
            break

    if type_ == 'add_bird' and (typebird == "green" or typebird == "yellow" or typebird == 'brown' or typebird == 'blue'):
        anality['Birds'].append({
            'name': Birds.Birdtypes[typebird].name,
            'productivity': Birds.Birdtypes[typebird].productivity,
            'eggs': Birds.Birdtypes[typebird].eggs
        })
    elif type_ == 'add_balance' and balance != 0 and anality['type'] == 'admin':
        pass
    with open("balances.json", 'w', encoding='utf8') as file:
        json.dump(data, file, indent=2, ensure_ascii=False)


def save_user_data(balances):
    data = json.load(open("balances.json", encoding="utf8"))
    for i in data["personal"]:
        if balances.get('id') == i.get('id'):
            return
    data["personal"].append(balances)
    try:
        with open('balances.json', 'w') as file:
            json.dump(data, file, indent=2, ensure_ascii=False)
    except FileNotFoundError:
        return 0


def add_balance(user_id, balance):
    data = json.load(open('balances.json', encoding='utf8'))
    for i in data['personal']:
        if user_id == i.get('id') and i.get('type') == 'admin':
            i['balance'] += balance
            print(i['balance'])
            break
    with open("balances.json", 'w', encoding='utf8') as file:
        json.dump(data, file, indent=2, ensure_ascii=False)


def add_admin(user_id):
    data = json.load(open('balances.json', encoding='utf8'))
    for i in data['personal']:
        if user_id == i.get('id'):
            i['type'] = 'admin'
    with open("balances.json", 'w', encoding='utf8') as file:
        json.dump(data, file, indent=2, ensure_ascii=False)

def BirdAction():
    info = json.load(open("balances.json", encoding="utf8"))

    for person in info["personal"]:
        for bird_info in person["Birds"]:
            bird_type = Birds.Birdtypes.get(bird_info["name"])
            if bird_type:
                bird_info["eggs"] = bird_info['eggs'] + bird_type.update()

    with open("balances.json", 'w', encoding='utf8') as file:
        json.dump(info, file, indent=2, ensure_ascii=False)
