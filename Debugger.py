enabled = True
def debugger(func):
    def wrapper(text):
        if enabled:
            func(text)
    return wrapper

@debugger
def debugger_print(text):
    print(text)
