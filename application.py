from flask import Flask, render_template, request, redirect, session
import sqlite3 as sql

# database pleasantries

def cursor():
    return sql.connect('db.sqlite3').cursor()

def run_sql(command):
    c = cursor()
    with c.connection:
        return c.execute(command)

run_sql(
    '''CREATE TABLE IF NOT EXISTS "shopping_list" (
        "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
        "item_name" varchar(15) UNIQUE NOT NULL,
        "acquired" bool NOT NULL,
        "on_list" bool NOT NULL,
    );''')

# objects

class ListItem:
    def __init__(self, name):
        if name != "" and name != None:
            self.name = name.strip().lower()
            self.acquired = 0
            self.on_list = 1
    
    def add(self):
        run_sql(f'''INSERT INTO "shopping_list" ("item_name", "acquired", "on_list")
                    VALUES ("{self.name}", {self.acquired}, {self.on_list});''')

    @classmethod
    def checkbox(cls, id, value):
        run_sql(f'''UPDATE "shopping_list" 
                    SET "acquired" = {value}
                    WHERE "id" = {id};''')
    
    @classmethod
    def delete(cls, id):
        run_sql(f'''UPDATE "shopping_list" 
                    SET "on_list" = 0
                    WHERE "id" = {id};''')
    
    @classmethod
    def turn_on(cls, id):
        run_sql(f'''UPDATE "shopping_list" 
                    SET "on_list" = 1
                    WHERE "id" = {id};''')       

    @classmethod
    def rename(cls, oldname, newname):
        run_sql(f'''UPDATE "shopping_list" 
                    SET "item" = "{newname.lower()}"
                    WHERE "item" = "{oldname.lower()}";''')

    @classmethod
    def all(cls):
        output_list = []
        for v in run_sql('SELECT * FROM "shopping_list";'):
            v = (v[0], v[1].capitalize(), v[2], v[3])
            output_list.append(v)
        return output_list

    @classmethod
    def active(cls):
        output_list = []
        for v in run_sql('SELECT * FROM "shopping_list";'):
            v = (v[0], v[1].capitalize(), v[2], v[3])
            if v[3] == 1:
                output_list.append(v)
        return output_list        

    def __str__(self):
        return self.name

# application / views

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    shopping_list = ListItem.all()[::-1]
    flag = True if ListItem.active() != [] else False
    if request.method == "GET":
        return render_template("index.html", shopping_list=shopping_list, flag=flag)
    elif request.method == "POST":
        item_name = request.form.get("shopping-list-item")
        if item_name != "" and item_name != None:
            for item in shopping_list:
                if item[1].lower() == item_name.strip().lower():
                    ListItem.turn_on(item[0])
                else:
                    try:
                        ListItem(name=item_name).add()
                    except:
                        pass
        for item in shopping_list:
            if request.form.get(f'checkbox-{item[0]}') == None:
                ListItem.checkbox(item[0], 0)
            else:
                ListItem.checkbox(item[0], 1)
            if request.form.get(f'deletebox-{item[0]}') == None:
                pass
            else:            
                ListItem.delete(item[0])
        return redirect("/")
