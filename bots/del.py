
    args_in = {'a': 10, 'b': 11, 'c': 55, 'd': 12, 'e': 33}

    def func1(**kwargs):
        d = kwargs.get('d')
        e = kwargs.get('e')

        print 'Func1:'
        print d + e

    def func2(**kwargs):
        a = kwargs.get('a')
        b = kwargs.get('b')
        c = kwargs.get('c')

        print 'func2:'
        print a + b + c

        func1(**kwargs)


    func2(**args_in)
