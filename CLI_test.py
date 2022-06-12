from CLI import *
import unittest
import sys
import os


class TestMutableList(unittest.TestCase):
    def test_version(self):
        lst = ['-v', '-V', '--version']
        for s in lst:
            res = version()
            self.assertEqual(res, sys.version)

    def test_path(self):
        lst = [['PATH', '1.txt'], ['PATH', '2.txt']]
        for s in lst:
            res = PATH(s[1])
            self.assertEqual(res, os.getcwd() + '\\' + s[1])

    def test_help(self):
        lst = ['usage',
               'sub_commands',
               'position_arguments',
               'named_arguments']
        self.assertEqual(Help(lst[0]), 'usage: \n [--version | -V |-v ] '
                                       '[-h] [PATH] '
                                       '[-r][cat a|n|d] '
                                       '[-hex]')
        self.assertEqual(Help(lst[1]), 'sub_commands: \n cat a: add '
                                       'data to the file '
                                       '\n cat n: create a new file'
                                       '\n cat d: delete files')
        self.assertEqual(Help(lst[2]), 'position_arguments: '
                                       '\n PATH : Print the '
                                       'absolute path of the file')
        self.assertEqual(Help(lst[3]), 'named_arguments: \n --version : '
                                       'Show the current command_line '
                                       'interface version(also -v -V) '
                                       '\n -h: show this help method and exit '
                                       '\n -r: Read the contents in the file '
                                       '\n -hex: Change the input value to '
                                       'hex and save it to the hex.txt')

    def test_cat_a(self):
        add_content = 'cpo-ddd'
        lst = ['cat', 'a', '1.txt', add_content]
        f1 = open('1.txt')
        original_content = f1.read()
        f1.close()
        cat(lst[1:])
        f2 = open('1.txt')
        new_content = original_content + add_content + '\n'
        self.assertEqual(new_content, f2.read())
        f2.close()

    def test_cat_n(self):
        if os.path.exists('new.txt'):
            os.remove('new.txt')
        lst = ['cat', 'n', 'new.txt']
        cat(lst[1:])
        flag = os.path.exists('new.txt')
        self.assertEqual(True, flag)

    def test_cat_d(self):
        if os.path.exists('file.txt'):
            os.remove('file.txt')
        lst1 = ['cat', 'n', 'new.txt']
        cat(lst1[1:])
        flag = os.path.exists('new.txt')
        self.assertEqual(True, flag)
        lst2 = ['cat', 'd', 'new.txt']
        cat(lst2[1:])
        flag = os.path.exists('new.txt')
        self.assertEqual(False, flag)

    def test_hex(self):
        lst = ['hex', 10]
        f = open('hex.txt', 'r+')
        f.truncate()
        hex(lst[1])
        self.assertEqual('a' + '\n', f.read())
        f.close()

        lst = ['hex', 14]
        f = open('hex.txt', 'r+')
        f.truncate()
        hex(lst[1])
        self.assertEqual('e' + '\n', f.read())
        f.close()

    def test_read(self):
        lst = ['-r', '1.txt']
        f1 = open('1.txt')
        res = read(lst[1])
        self.assertEqual(res, f1.readlines())
        f1.close()


if __name__ == '__main__':
    unittest.main()
