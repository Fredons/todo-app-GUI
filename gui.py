import functions
import PySimpleGUI as sg
import time
import os

if not os.path.exists('todos.txt'):
    with open("todos.txt", 'w') as file:
        pass

sg.theme("TanBlue")

clock = sg.Text("", key='clock')
label = sg.Text("Type in a to-do")
input_box = sg.InputText(tooltip="Enter todo", key="todo")
add_button = sg.Button("Add", tooltip="Add todo")
list_box = sg.Listbox(values=functions.get_todos(), key="todos",
                      enable_events=True, size=[45, 10])
edit_button = sg.Button("Edit")
complete_button = sg.Button("Complete")

exit_button = sg.Button("Exit")

window = sg.Window("My Todo App",
                   layout=[[clock],
                           [label],
                           [input_box, add_button],
                           [list_box, edit_button, complete_button],
                           [exit_button]],
                   font=('Helvetica', 20))

while True:
    event, value = window.read(timeout=250)
    window['clock'].update(value=time.strftime('%d - %b - %Y   %H:%M:%S'))

    match event:
        case "Add":
            todo_text = value['todo'].strip()  # Remove leading and trailing whitespace
            if todo_text:  # Check if the input is not empty
                todos = functions.get_todos()
                new_todo = value['todo'] + '\n'
                todos.append(new_todo)
                functions.write_todos(todos)
                window['todos'].update(values=todos)
            else:
                sg.popup("Cannot add an empty to-do. Please enter a task.", font=("Helvetica", 20))
        case sg.WINDOW_CLOSED:
            break

        case "Edit":
            try:
                todos = functions.get_todos()
                if todos:
                    todo_to_edit = value['todos'][0]
                    new_todo = value['todo']
                    index = todos.index(todo_to_edit)
                    if todos[index] == new_todo:
                        sg.popup("Task still the same. No edit made!")
                    else:
                        todos[index] = new_todo + '\n'
                        functions.write_todos(todos)
                        window['todos'].update(values=todos)
                else:
                    sg.popup("There are no items to edit.", font=("Helvetica", 20))
            except IndexError:
                sg.popup("Please select an item first", font=("Helvetica", 20))

        case "Complete":
            try:
                todos = functions.get_todos()
                if todos:
                    todo_to_complete = value['todos'][0]
                    todos.remove(todo_to_complete)
                    functions.write_todos(todos)
                    window['todos'].update(values=todos)
                    window['todo'].update(value="")
                else:
                    sg.popup("There are no items to complete.", font=("Helvetica", 20))
            except IndexError:
                sg.popup("Please select an item first", font=("Helvetica", 20))

        case 'todos':
            if value['todos']:
                window['todo'].update(value['todos'][0])

        case "Exit":
            break

window.close()
