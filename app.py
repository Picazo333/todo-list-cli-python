import csv
import os

todos = []
stop = False
TODOS_PATH = "todos.csv"


def get_todos():
    global todos
    return todos


def add_one_task(title):
    global todos
    todos.append(title)


def print_list():
    global todos
    if len(todos) == 0:
        print("No tasks yet. Choose option 1 to add one. Example: Make the bed")
        return
    for index, task in enumerate(todos, start=1):
        print(f"{index}. {task}")


def delete_task(number_to_delete):
    global todos
    try:
        position = int(number_to_delete)
    except (TypeError, ValueError):
        print("Invalid position: enter a whole number from the list, for example 1.")
        return False
    if position < 1 or position > len(todos):
        if len(todos) == 0:
            print("Invalid position: the list is empty. Choose option 1 to add a task first.")
        else:
            print(
                f"Invalid position: {position} is outside 1-{len(todos)}. "
                "Choose option 3 to see current positions."
            )
        return False
    todos.pop(position - 1)
    return True


def save_todos():
    global todos
    try:
        with open(TODOS_PATH, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file, lineterminator="\n")
            for title in todos:
                writer.writerow([title])
    except OSError as error:
        print(f"Cannot save tasks to {TODOS_PATH}: {error}")
        return False
    return True


def load_todos():
    global todos
    if not os.path.exists(TODOS_PATH):
        print(
            f"Cannot load tasks: {TODOS_PATH} does not exist. "
            "The current list was not changed."
        )
        return False
    try:
        with open(TODOS_PATH, "r", encoding="utf-8", newline="") as file:
            raw = file.read()
    except UnicodeError:
        print(
            f"Cannot load tasks: {TODOS_PATH} is not valid UTF-8. "
            "The current list was not changed."
        )
        return False
    except OSError as error:
        print(f"Cannot load tasks: {error}. The current list was not changed.")
        return False
    if raw == "":
        todos = []
        return True
    if "\x00" in raw:
        print(
            f"Cannot load tasks: {TODOS_PATH} is not a text file. "
            "The current list was not changed."
        )
        return False
    try:
        rows = list(csv.reader(raw.splitlines()))
    except csv.Error:
        print(
            f"Cannot load tasks: {TODOS_PATH} is not valid CSV. "
            "The current list was not changed."
        )
        return False
    loaded = []
    for row in rows:
        if len(row) == 0:
            continue
        if len(row) != 1:
            print(
                f"Cannot load tasks: {TODOS_PATH} has a row with more than one column. "
                "The current list was not changed."
            )
            return False
        loaded.append(row[0])
    todos = loaded
    return True


def print_help():
    print("Commands:")
    print("  1  Add a task. Example title: Make the bed")
    print("  2  Delete by the number shown in the list. Example: 2")
    print("  3  Show every task with its position, starting at 1")
    print("  4  Save the current list to todos.csv")
    print("  5  Replace the current list with the tasks in todos.csv")
    print("  6  Exit")
    print("  help  Show this guide")
    print("There is no edit command. Delete the task and add it again.")
    print("A delete renumbers the tasks that follow it.")


def _read_line():
    try:
        return input()
    except EOFError:
        print()
        return None


# Below this code will only run if the entry file running was app.py
if __name__ == '__main__':
    while stop == False:
        print("""
    Choose an option: 
        1. Add one task
        2. Delete a task
        3. Print the current list of tasks
        4. Save todo's to todos.csv
        5. Load todo's from todos.csv
        6. Exit
    """)
        print("    Type help for examples. Positions start at 1.")
        response = _read_line()
        if response is None:
            stop = True
            continue
        response = response.strip()
        if response == "6":
            stop = True
        elif response == "3":
            print_list()
        elif response == "2":
            print("What task number you want to delete?")
            number_to_delete = _read_line()
            if number_to_delete is None:
                stop = True
                continue
            if delete_task(number_to_delete.strip()):
                print("Task removed. Positions were updated:")
                print_list()
        elif response == "1":
            print("What is your task title?")
            title = _read_line()
            if title is None:
                stop = True
                continue
            if title.strip() == "":
                print("Task title cannot be empty. Example: Make the bed")
            else:
                add_one_task(title)
                print(f"Added {len(todos)}. {title}")
                print_list()
        elif response == "4":
            print("Saving todo's...")
            if save_todos():
                count = len(todos)
                noun = "task" if count == 1 else "tasks"
                print(f"Saved {count} {noun} in todos.csv.")
        elif response == "5":
            print("Loading todo's...")
            if load_todos():
                count = len(todos)
                noun = "task" if count == 1 else "tasks"
                print(f"Loaded {count} {noun} from todos.csv.")
                print_list()
        elif response.lower() in ("help", "?"):
            print_help()
        else:
            print("Invalid response, asking again...")
            print("Type help to see each option with an example.")
