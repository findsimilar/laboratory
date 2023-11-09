class Printer:
    """
    This class decorator save results to some place (default print its)
    """

    def __init__(self, title=None, printer=print):
        """
        Init
        :title: callback with title -> title()
        :printer: print function (default print)
        """
        self.title = title
        self.printer = printer

    def __call__(self, func):
        """
        Make decorator
        :func: decorated function
        """
        def inner(*args, **kwargs):
            """
            New function
            """
            printer = kwargs.get('printer', self.printer)

            if 'printer' in kwargs:
                is_delete_printer = True
                if 'is_pass_printer' in kwargs:
                    if kwargs['is_pass_printer']:
                        is_delete_printer = False
                    del kwargs['is_pass_printer']

                if is_delete_printer:
                    del kwargs['printer']

            printer('Start')
            if self.title is not None:
                printer(self.title(*args, **kwargs))
            result = func(*args, **kwargs)
            printer('Done:')
            printer(result)
            printer('End')
            return result

        return inner
