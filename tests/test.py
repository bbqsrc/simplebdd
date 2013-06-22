import simplebdd
from simplebdd import Description, Context, async
from time import sleep

class List(Description):
    """List"""

    class AList(Context):
        """A list"""

        def it_has_the_type_list(self):
            """has the type 'list'"""
            return isinstance([], list)

        def it_makes_rum(self):
            """has a distillery embedded"""
            pass

        class WithThreeElements(Context):
            """with three elements"""

            def before_tests(self):
                self.list = [1, 2, 3]

            @async
            def it_has_a_length_of_3(self):
                """has a length of 3"""
                return len(self.list) == 3

        class WithZeroElements(Context):
            """with zero elements"""

            def before_tests(self):
                self.list = []

            @async
            def it_has_a_length_of_0(self):
                """has a length of zero"""
                return len(self.list) == 0

            @async
            def it_returns_exception_when_popped(self):
                """returns Exception when pop()'d"""
                try:
                    self.list.pop()
                except IndexError as e:
                    return True
                return False

