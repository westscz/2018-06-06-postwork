import cmd, sys
import turtle


class BaseComposite(object):
    def __repr__(self):
        raise NotImplementedError

    def eval(self):
        raise NotImplementedError


class Leaf(BaseComposite):
    def __init__(self, arg=''):
        self.arg = arg

    def __repr__(self):
        return self.__class__.__name__


class LeafArg(Leaf):
    def __repr__(self):
        return "{} {}".format(self.__class__.__name__, self.arg)


class Compound(BaseComposite):
    pass


class Forward(LeafArg):
    def eval(self):
        'Move the turtle forward by the specified distance:  FORWARD 10'
        turtle.forward(int(self.arg))


class Right(LeafArg):
    def eval(self):
        'Turn turtle right by given number of degrees:  RIGHT 20'
        turtle.right(int(self.arg))


class Left(LeafArg):
    def eval(self):
        'Turn turtle left by given number of degrees:  LEFT 90'
        turtle.left(int(self.arg))


class Home(Leaf):
    def eval(self):
        'Return turtle to the home position:  HOME'
        turtle.home()


class Circle(LeafArg):
    def eval(self):
        'Draw circle with given radius an options extent and steps:  CIRCLE 50'
        turtle.circle(int(self.arg))


class Position(Leaf):
    def eval(self):
        'Print the current turtle position:  POSITION'
        print('Current position is %d %d\n' % turtle.position())


class Heading(Leaf):
    def eval(self):
        'Print the current turtle heading in degrees:  HEADING'
        print('Current heading is %d\n' % (turtle.heading(),))


class Reset(Leaf):
    def eval(self):
        'Clear the screen and return turtle to center:  RESET'
        turtle.reset()


class Bye(Leaf):
    def eval(self):
        'Close the turtle window, and exit:  BYE'
        print('Thank you for using Turtle')
        turtle.bye()
        return True


class Run(Compound):
    def __init__(self, first, second):
        self._first = first
        self._second = second

    def eval(self):
        self._first.eval()
        self._second.eval()

    def __repr__(self):
        return "{} -> {}".format(self._first, self._second)


class TurtleCmd(object):
    # ----- basic turtle commands -----
    forward = Forward
    right = Right
    left = Left
    home = Home
    circle = Circle
    position = Position
    heading = Heading
    reset = Reset
    bye = Bye


class TurtleShell(cmd.Cmd):
    intro = 'Welcome to the turtle shell.   Type help or ? to list commands.\n'
    prompt = '(turtle) '

    def __init__(self):
        cmd.Cmd.__init__(self)
        self._history = None
        self._record = False

        self.tcmd = TurtleCmd()

    def do_record(self, arg):
        'rozpoczyna nagrywanie makra'
        self._record = True
        self._history = []

    def do_stop(self, arg):
        'konczy nagrywanie makra'
        self._record = False

    def do_playback(self, arg):
        'wykonuje makro, tzn. wszystkie komendy po komendzie "record", az do komendy "stop". '
        loop = int(arg) if arg else 1
        for cmd in loop * self._history:
            self.onecmd(cmd)

    def default(self, line):
        cmd, arg, line = self.parseline(line)
        try:
            func = getattr(self.tcmd, cmd)
            if self._record:
                self._history.append(line)
            return func(arg).eval()
        except AttributeError:
            self.stdout.write('*** Unknown syntax: %s\n' % line)


if __name__ == '__main__':
    TurtleShell().cmdloop()

    # expr = Run(Run(Home(), Right(45)), Run(Forward(50), Circle(45)))
    # print(repr(expr))
    # expr.eval()
