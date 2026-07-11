import cmd

class ComputerAlegbraSystem(cmd.Cmd):
    
    intro = "Computer Algebra REPL in Python."
    prompt = "> "

    def default(self, line):
        """Run line."""
        return run(line)


    def do_quit(self, line):
        """Exit the REPL."""
        return True


def run(user_input):
    print(user_input)


if __name__ == "__main__":
    ComputerAlegbraSystem().cmdloop()