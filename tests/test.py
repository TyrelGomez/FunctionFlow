from FunctionFlow import repeat, repeat_until, exitFunctionIf, skipToFunction, sleep, is_paused, pause_sleep, unpause, run_list

x = 0

@repeat_until(lambda: x == 4)
def increment_x():
    global x
    x += 1
    print(x)

@run_list(lambda: increment_x())
def doitfirst():
    print("This should run first")

doitfirst()
