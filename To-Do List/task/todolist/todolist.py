from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from datetime import *
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


# create table for db
class Table(Base):
    __tablename__ = 'task'
    id = Column('id', Integer, primary_key=True)
    task = Column('task', String)
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return self.task


engine = create_engine('sqlite:///todo.db?check_same_thread=False')
Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)
session = Session()

Menu = "1) Today's tasks\n" \
       "2) Week's tasks\n" \
       "3) All tasks\n" \
       "4) Missed tasks\n" \
       "5) Add task\n" \
       "6) Delete task\n" \
       "0) Exit"


# check if you have tasks today
def todays_task():
    today = datetime.today()
    rows = session.query(Table).filter(Table.deadline == today.date()).all()
    if len(rows) == 0:
        print("Today " + today.strftime("%d %b") + ": \nNothing to do!\n")
    else:
        print("Today " + today.strftime("%d %b") + ": ")
        for row in rows:
            print(str(row.id) + ". " + row.task)
        print()


# check your tasks for this week
def weeks_task():
    today = datetime.today()
    for i in range(7):
        week = today + timedelta(days=i)
        rows = session.query(Table).filter(Table.deadline == week.date()).all()
        print(week.strftime("%A %d %b") + ":")
        if len(rows) == 0:
            print("Nothing to do!\n")
        else:
            i = 1
            for row in rows:
                print(str(i) + ". " + row.task)
                i += 1
            print()


# check all tasks that you have to do
def all_task():
    rows = session.query(Table).order_by(Table.deadline).all()
    if len(rows) == 0:
        print("All tasks: \nNothing to do!\n")
    else:
        print("All tasks: ")
        i = 1
        for row in rows:
            print(str(i) + ". " + row.task + ". " + row.deadline.strftime("%d %b"))
            i += 1
        print()

        
# check if you missed any task
def missed():
    rows = session.query(Table).filter(Table.deadline < datetime.today().date()).all()
    print("Missed tasks:")
    if len(rows) == 0:
        print("Nothing is missed!\n")
    else:
        i = 1
        for row in rows:
            print(str(i) + ". " + row.task + ". " + row.deadline.strftime("%d %b"))
            i += 1
        print()

        
# add new task with deadline
def add_task():
    task_input = input("Enter task \n")
    deadline_input = input("Enter deadline \n")
    new_row = Table(task=task_input, deadline=datetime.strptime(deadline_input, '%Y-%m-%d').date())
    session.add(new_row)
    session.commit()
    print("The task has been added!")

    
# delete tasks that you don't need anymore
def delete():
    rows = session.query(Table).order_by(Table.deadline).all()
    print("Choose the number of the task you want to delete:")
    i = 1
    i_id = {}
    for row in rows:
        print(str(i) + ". " + row.task + ". " + row.deadline.strftime("%d %b"))
        i_id[i] = row.id
        i += 1
    print(i_id)
    del_action = int(input())
    session.query(Table).filter(Table.id == i_id[del_action]).delete()
    session.commit()
    print("The task has been deleted!\n")


while True:
    user_action = input(Menu + "\n")
    if user_action == '1':
        todays_task()
    elif user_action == '2':
        weeks_task()
    elif user_action == '3':
        all_task()
    elif user_action == '4':
        missed()
    elif user_action == '5':
        add_task()
    elif user_action == '6':
        delete()
    elif user_action == '0':
        break

session.close()
