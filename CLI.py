import sys
import os
from functools import wraps
from typing import List, Callable, Dict


def v():
    """
    Function description: Output version information
    """
    ret = sys.version
    print(ret)
    return ret


def PATH(s: str) -> str:
    """
    Function description: Output the path of the specified file
    :param s: Command entered
    """
    path = os.getcwd()
    ret = path + '\\' + s
    print(ret)
    return ret


def Help(s: str) -> str:
    """
    Function description: Output help information
    :param s: Command entered
    """
    if s in ['usage',
             'sub_commands',
             'position_arguments',
             'named_arguments']:
        result = s + ': '
        if s == 'usage':
            result = result + '\n [--version | -V |-v ] ' \
                              '[-h] [PATH] ' \
                              '[-r][cat a|n|d] ' \
                              '[-hex]'
        elif s == 'sub_commands':
            result = result + '\n cat a: add data to the file' \
                              ' \n cat n: create a new file\n' \
                              ' cat d: delete files'
        elif s == 'position_arguments':
            result = result + '\n PATH : Print the ' \
                              'absolute path of the file'
        elif s == 'named_arguments':
            result = result + '\n --version : Show the current ' \
                              'command_line interface version(also -v -V) \n' \
                              ' -h: show this help method and exit \n' \
                              ' -r: Read the contents in the file \n' \
                              ' -hex: Change the input value ' \
                              'to hex and save it to the hex.txt'
    else:
        result = 'no help topic match ' + s
    print(result)
    return result


def read(s: str) -> List[str]:
    """
    Function description: Read the contents in the file
    :param s: Command entered
    """
    with open(s) as f:
        lines = f.readlines()
        for i in lines:
            print(i, end='')
        return lines


def cat(s: List) -> None:
    """
    Function description:
            cat a: add data to the file
            cat n: create a new file
            cat d: Download files via http
    :param s: Command entered
    """
    while len(s) > 0 and s[0] in ['n', 'a', 'd']:
        if s[0] == 'n':
            s.pop(0)
            f = open(s[0], 'w')
            f.close()
            s.pop(0)
        elif s[0] == 'a':
            s.pop(0)
            with open(s[0], 'a') as f:
                f.write(s[1] + "\n")
            s = s[2:]
        elif s[0] == 'd':
            s.pop(0)
            if os.path.exists(s[0]):
                os.remove(s[0])
            s.pop(0)


def hex(s: str) -> str:
    """
    Function description: Change the input
    value to hex and save it to the hex.txt
    :param s: Command entered
    """
    ret = ""
    hex1 = ['0', '1', '2', '3', '4', '5', '6',
            '7', '8', '9', 'a', 'b', 'c', 'd',
            'e', 'f']
    num = int(s)
    while num > 15:
        ret = hex1[num % 16] + ret
        num = num // 16
    ret = hex1[num] + ret
    with open('hex.txt', 'a') as f:
        f.write(ret + "\n")
    print(ret)
    return ret


class CLIDecorator(object):
    def __init__(self, name: str) -> None:
        print(name)
        self.fun = {'-v': v,
                    '-V': v,
                    '--version': v,
                    'PATH': PATH,
                    '-h': Help,
                    '-r': read,
                    'cat': cat,
                    '-hex': hex}
        self.subcommand_name = []  # type: List
        self.Coms = []  # type: List
        self.option_command = {}  # type: Dict

    def command(self, f: Callable) -> Callable:
        """
        Used to decorate a function so that
        the function serves as a command line interface
        :param f: Callable
        :return: Callable
        """

        def r(*args, **kwargs):
            self.Coms = sys.argv[1:]
            return f(*args, **kwargs)

        return r

    def option(self,
               func_name: str,
               default=None,
               Help=None) -> Callable:
        """
        Used to decorate a function
        :param func_name: str
        :param default: Union[str, None]
        :return: Callable
        """

        def logging_decorator(func):
            @wraps(func)
            def wrapped_function(*args, **kwargs):
                self.option_command[self.fun[func_name]] = default
                return func(*args, **kwargs)

            return wrapped_function

        return logging_decorator

    def argument(self,
                 func_name: str,
                 default=None,
                 Help=None) -> Callable:
        """
        Pass a simple variable value
        :param func_name: str
        :param default: Union[str, None]
        :return: Callable
        """

        def logging_decorator(func):
            @wraps(func)
            def wrapped_function(*args):
                argu = default
                self.subcommand_name.append(func_name)
                self.fun[func_name] = func_name
                self.option_command[self.fun[func_name]] = args
                self.Coms = sys.argv[1:]
                if func_name in self.Coms:
                    index = self.Coms.index(func_name)
                    if len(self.Coms) == 1:
                        argu = None
                    else:
                        argu = self.Coms[index + 1]
                func(argu)

            return wrapped_function

        return logging_decorator

    def run(self) -> None:
        while len(self.Coms) > 0:
            if self.fun[self.Coms[0]] not in self.option_command:
                print('\'' + self.Coms[0] + '\' is not availiable')
                raise KeyError
                break
            elif self.fun[self.Coms[0]] is v:
                # print(self.Coms)
                v()
                self.Coms = self.Coms[1:]
            elif self.fun[self.Coms[0]] is Help:
                Help(self.Coms[1])
                self.Coms = self.Coms[2:]
            elif self.fun[self.Coms[0]] in self.subcommand_name:
                break
            elif self.fun[self.Coms[0]] is PATH:
                if len(self.Coms) == 1:
                    PATH(self.option_command[PATH])
                    break
                elif self.Coms[1] in self.fun:
                    PATH(self.option_command[PATH])
                    self.Coms = self.Coms[1:]
                else:
                    PATH(self.Coms[1])
                    self.Coms = self.Coms[2:]
            elif self.fun[self.Coms[0]] is read:
                if len(self.Coms) == 1:
                    read(self.option_command[read])
                    break
                elif self.Coms[1] in self.fun:
                    read(self.option_command[read])
                    self.Coms = self.Coms[1:]
                else:
                    read(self.Coms[1])
                    self.Coms = self.Coms[2:]
            elif self.fun[self.Coms[0]] is hex:
                if len(self.Coms) == 1:
                    hex(self.option_command[hex])
                    break
                elif self.Coms[1] in self.fun:
                    hex(self.option_command[hex])
                    self.Coms = self.Coms[1:]
                else:
                    hex(self.Coms[1])
                    self.Coms = self.Coms[2:]
            elif self.fun[self.Coms[0]] is cat:
                if len(self.Coms) == 1 or self.Coms[1] in self.fun:
                    print('Invalid instruction ')
                else:
                    c = []
                    self.Coms.pop(0)
                    while self.Coms[0] in ['n', 'a', 'd']:
                        if self.Coms[0] == 'a':
                            c.append(self.Coms[0])
                            self.Coms.pop(0)
                            c.append(self.Coms[0])
                            self.Coms.pop(0)
                            c.append(self.Coms[0])
                            self.Coms.pop(0)
                        else:
                            c.append(self.Coms[0])
                            self.Coms.pop(0)
                            c.append(self.Coms[0])
                            self.Coms.pop(0)
                        if len(self.Coms) == 0:
                            break
                    cat(c)
