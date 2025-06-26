from cli.cmd import HonulabsCommandPrompt

cli = HonulabsCommandPrompt()
try:
    cli.cmdloop()
except (KeyboardInterrupt, EOFError):
    pass
