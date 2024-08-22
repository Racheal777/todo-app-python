import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()


def connect():
    try:
        return psycopg2.connect(host=os.getenv('HOSTNAME'),
                                dbname=os.getenv('DATABASE'),
                                user=os.getenv('USERNAME', 'postgres'),
                                password=os.getenv('PASSWORD'),
                                port=os.getenv('PORT'))
    except:
        return False


conn = connect()


def create_table():
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE tasks (id Serial PRIMARY KEY, task varchar(255), status bool default false)', )
    conn.commit()
    cursor.close()


def add_task(task):
    cursor = conn.cursor()
    cursor.execute('INSERT INTO tasks(task) VALUES (%s)', (task,))
    conn.commit()
    print(f"Todo -  {task}  has been added ")
    cursor.close()


def display_tasks():
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM tasks ORDER BY status DESC')
    results = cursor.fetchall()

    for id, task, status in results:
        print(f"Todo - id- {id},  {task} :  Status - {status} ")

    cursor.close()


def update_task_status(taskId):
    cursor = conn.cursor()
    if not taskId:
        print('Enter an id')
        return 'ID not available'
    find_task = cursor.execute('SELECT * from tasks WHERE id = (%s)', (taskId,))
    if not find_task:
        print(f" task wit the id {taskId} does not exist")
        return 'Task not found'
    cursor.execute('UPDATE tasks SET status = true WHERE id = (%s)', (taskId,))
    conn.commit()
    print(f"Todo with id   {taskId}  status has been updated ")
    cursor.close()


def main():
    print("\n My ToDo App")
    print("1. Add a todo")
    print("2. Display all todos")
    print("3. update status of a todo")
    print("4. Exit")

    while True:

        try:
            choice = int(input("Choose an option > "))
            if choice == 1:
                todo = input("Add your todo > ")
                add_task(todo)
            elif choice == 2:
                display_tasks()
            elif choice == 3:
                todoId = input("Enter a todo id to update the status > ")
                update_task_status(todoId)

            elif choice == 4:
                print('exited')
                break
            else:
                print('option is not allowed, choose again > ')
        except ValueError:
            print('please enter a valid')


if __name__ == "__main__":
    main()
