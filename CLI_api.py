from CLI import CLIDecorator
import os

cli = CLIDecorator("Welcome to CLI_api.")


@cli.command
@cli.option('-v', default=None, Help='vision')
@cli.option('-h', default=None, Help='help information')
@cli.option('PATH', default=' ', Help='get the file\'s path')
@cli.option('-r', default='1.txt', Help='read file')
@cli.option('-hex', default='0',
            Help='Change the input value '
                 'to hex and save it to the hex.txt')
@cli.option('cat', default=None, Help='This is a subcommand')
@cli.argument('name', default='', Help='your hello')
def hello(name=None):
    if name is not None:
        print('Hello ' + name)
    else:
        print('Hello...')


if __name__ == '__main__':
    hello()
    cli.run()
