from simplebdd import Test, Description, async, NoOutput


class SimpleBDDTests(Test):
    def before_each_test(self):
        self.test_mock1 = self.TestMock1()
        self.test_mock1.run(NoOutput())

        self.test_mock2 = self.TestMock2()
        self.test_mock2.run(NoOutput())

    class HelperMethods(Description):
        """Helper methods"""

        def it_should_trigger_before_each_test(self):
            """it should trigger before_each_test"""
            return self.test.test_mock1.triggered.count('before_each_test') == 4

        def it_should_trigger_after_each_test(self):
            """it should trigger after_each_test"""
            return self.test.test_mock1.triggered.count('after_each_test') == 4

        def it_should_trigger_before_tests(self):
            """it should trigger before_tests"""
            return self.test.test_mock1.triggered[0] == 'before_tests'

        def it_should_trigger_after_tests(self):
            """it should trigger after_tests"""
            return self.test.test_mock1.triggered[-1] == 'after_tests'

    class BaselineFunctionality(Description):
        """Baseline functionality"""

        def it_should_pass_tests_when_true_returned(self):
            """It should pass tests when True returned"""
            return self.test.test_mock1.results[0] == (1,0,0)

        def it_should_fail_tests_when_false_returned(self):
            """It should fail tests when False returned"""
            return self.test.test_mock1.results[1] == (1,1,0)

        def it_should_pend_tests_when_anything_else_returned(self):
            """It should pend tests when anything else returned"""
            return self.test.test_mock1.results[2] == (1,1,1)

        def it_should_fail_tests_when_exception_raised(self):
            """It should fail tests when exception raised"""
            return self.test.test_mock1.results[3] == (1,2,1)

    class AsyncFunctionality(Description):
        """Asynchronous functionality"""

        def it_should_record_test_results_when_async(self):
            return self.test.test_mock2.passes == 1 and\
                self.test.test_mock2.fails == 1 and\
                self.test.test_mock2.pending == 1

    # Test mock - needs to be here so it doesn't get autorun by script
    class TestMock1(Test):
        class Tests(Description):
            def before_tests(self):
                self.test.triggered = []
                self.test.triggered.append("before_tests")
                self.test.results = []

            def before_each_test(self):
                self.test.triggered.append("before_each_test")

            def after_each_test(self):
                self.test.triggered.append("after_each_test")
                self.test.results.append((self.test.passes, self.test.fails, self.test.pending))

            def after_tests(self):
                self.test.triggered.append("after_tests")

            def it_should_pass(self):
                """It should pass"""
                return True

            def it_should_fail(self):
                """It should fail"""
                return False

            def it_should_pend(self):
                """It should pend"""
                pass

            def it_should_except(self):
                """It should except"""
                raise Exception()

    class TestMock2(Test):
        class Tests(Description):
            @async
            def it_should_pass_async(self):
                return True

            @async
            def it_should_fail_async(self):
                return False

            @async
            def it_should_pend_async(self):
                return None
