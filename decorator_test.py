
def decorator_func(f):
    def func(x):
        count = count + x
        print("Decorator called")
        print(count)
        f()
    return func


@decorator_func
def do_something():
    print("do_something called")
