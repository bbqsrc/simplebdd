from simplebdd import Test, Description, async
from time import sleep

class ExampleTest(Test):
    class Examples(Description):
        """A set of example tests"""

        def it_should_exhibit_workingness(self):
            """it should exhibit that this works"""
            return True

        @async
        def it_should_fail(self):
            """it should fail"""
            return False

        @async
        def it_should_pend(self):
            """it should remain pending"""
            sleep(3)
            return None

        @async
        def it_should_attr_err(self):
            """it should attribute error"""
            self.foo

    class Examples2(Description):
        """A second set of examples"""
        def before_tests(self):
            self.foo = 42

        @async
        def it_should_have_42(self):
            """it should have a member foo with 42"""
            return getattr(self, 'foo', None) == 42

if __name__ == "__main__":
    ExampleTest().run()
