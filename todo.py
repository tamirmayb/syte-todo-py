import json
import sys
import os
from datetime import datetime

from pip._vendor.pep517.compat import FileNotFoundError


def _get_file(path):
    structure = '{"todo-list":[]}'
    with open(path, 'w') as f:
        f.write(structure)
    return structure


def _parse_data(data):
    if data:
        return json.loads(data)
    return ''


def _save_changes(data, file_name):
    dump = json.dumps(data)
    with open(file_name, 'w') as f:
        f.write(dump)


def _print_help():
    print('Usage: python todo.py [COMMAND] [INPUT]')
    print('\tCOMMAND:')
    print('\t\tadd - add task(INPUT will be added as task title, task will be displayed in red')
    print('\t\tdelete - delete task at INPUT index')
    print('\t\tdone - mark task at index INPUT as done, task will be displayed in blue')
    print('\t\tundone - mark task at index INPUT as undone, task will return to red from blue color')
    print('\tIf none was given tasks will be listed.')


class Todo(object):
    def __init__(self, file_name):
        self._file_name = file_name
        self._data_file = None
        self._changed = False
        self.red = '\033[31m'
        self.green = '\033[36m'
        self.no_color = '\033[0m'
        self._raw_data = self._get_file(self._file_name)
        self._parsed_data = _parse_data(self._raw_data)
        self.todos = self._parsed_data['todo-list']

    def _get_file(self, file_name):
        while not os.path.isfile(file_name):
            if os.getcwd() == '/':
                raise FileNotFoundError(
                    'File %s does not exist in path' % file_name)
            os.chdir('..')
        self._data_file = os.path.join(os.getcwd(), file_name)
        with open(os.path.join(os.getcwd(), file_name)) as data_file:
            data = data_file.read()
        if len(data):
            return data
        return _get_file(self._data_file)

    def _parse_data(self, todo, color):
        if color == 'red':
            print(self.red + todo + self.no_color)
        elif color == 'green':
            print(self.green + todo + self.no_color)
        else:
            print(todo)

    def _show_data(self, data):
        if not (data and len(data['todo-list'])):
            print('No tasks found.')
        else:
            for idx, task in enumerate(data['todo-list']):
                if task['is_done']:
                    self._parse_data(
                        '%s. [x] %s' % (idx, '| todo: ' + task['todo'] + ' | created: ' + task['created']), 'green')
                else:
                    self._parse_data('%s. [ ] %s' % (idx, '| todo: ' + task['todo'] +
                                                     ' | created: ' + task['created']), 'red')

    def _add_task(self, task):
        new_task = {
            'todo': task,
            'created': datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),
            'is_done': False
        }
        self.todos.append(new_task)
        self._changed = True

    def _delete_task(self, idx):
        if len(self.todos) <= idx:
            print('Out of range.')
        else:
            data = self.todos
            self._parsed_data['todo-list'] = data[:idx] + data[idx + 1:]
        self._changed = True

    def _done_task(self, idx):
        if len(self.todos) <= idx:
            print('Out of range')
        else:
            self.todos[idx]['is_done'] = True
        self._changed = True

    def _undone_task(self, idx):
        if len(self.todos) <= idx:
            print('Out of range')
        else:
            self.todos[idx]['is_done'] = False
        self._changed = True

    def run(self):

        if len(sys.argv) == 1:
            self._show_data(self._parsed_data)
        elif len(sys.argv) == 'usage':
            _print_help()
        elif sys.argv[1] == 'add':
            self._add_task(' '.join(sys.argv[2:]))
        elif sys.argv[1] == 'delete':
            self._delete_task(int(sys.argv[2]))
        elif sys.argv[1] == 'done':
            self._done_task(int(sys.argv[2]))
        elif sys.argv[1] == 'undone':
            self._undone_task(int(sys.argv[2]))
        else:
            _print_help()

        if self._changed:
            _save_changes(self._parsed_data, self._data_file)


def main():
    _todo = Todo('.todo-list.json')
    _todo.run()


if __name__ == '__main__':
    main()
