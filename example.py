import simplebdd

class ExampleTest(simplebdd.Test):
    class Examples(simplebdd.Description):
        """A set of example tests"""

        def pre_test(self):
            pass

        def post_test(self):
            pass

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

    class Examples2(simplebdd.Description):
        """A second set of examples"""

        def it_should_pass(self):
            """it should pass"""
            return True

if __name__ == "__main__":
    ExampleTest().run()
