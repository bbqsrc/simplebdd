from simplebdd import Test, Description

class ExampleTest(Test):
    class Examples(Description):
        """A set of example tests"""

        def it_should_exhibit_workingness(self):
            """it should exhibit that this works"""
            return True

        def it_should_fail(self):
            """it should fail"""
            return False

        def it_should_pend(self):
            """it should remain pending"""
            return None

        def it_should_attr_err(self):
            """it should attribute error"""
            self.foo

    class Examples2(Description):
        """A second set of examples"""
        def before_tests(self):
            self.foo = 42

        def it_should_have_42(self):
            """it should have a member foo with 42"""
            return getattr(self, 'foo', None) == 42

if __name__ == "__main__":
    ExampleTest().run()
