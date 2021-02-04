import os
import sys
import json
import tempfile
import unittest

from pip._vendor.pep517.compat import FileNotFoundError

from todo import Todo


class TestTodoList(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestTodoList, self).__init__(*args, **kwargs)
        self._test_file_name = '.todo-list.json'
        self.todo = Todo(self._test_file_name)
        with open(self._test_file_name) as f:
            self._test_file_content = f.read()

    def testGetFile(self):
        tmp_handler, tmp_path = tempfile.mkstemp()
        self.todo._get_file(tmp_path)
        with open(tmp_path, 'r') as f:
            tmp_content = f.read()
        self.assertEqual(tmp_content, '{"todo-list":[]}')

    def testReadData(self):
        self.assertEqual(self._test_file_content,
                         self.todo._get_file(self._test_file_name))
        self.assertRaises(FileNotFoundError,
                          lambda:
                          self.todo._get_file('ForSureThisDoesNotExist'))

    def testDeleteTask(self):
        self.todo._parsed_data = json.loads(self._test_file_content)
        l = len(self.todo._parsed_data['todo-list'])
        for i in range(1, l):
            self.todo._delete_task(0)
            self.assertEqual(len(self.todo._parsed_data), l-i)
        self.assertTrue(self.todo._changed)


def main():
    # set env
    install_dir = os.path.realpath(os.path.dirname(__file__))
    os.chdir(install_dir)
    sys.path.append('..')
    global todo
    import todo

    unittest.main()


if __name__ == "__main__":
    main()
