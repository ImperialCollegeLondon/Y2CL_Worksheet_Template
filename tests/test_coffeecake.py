from importlib import import_module
import pytest

@pytest.fixture(scope="module")
def cc():
    return import_module("src.coffeecake")

class TestTask10:
    def test_module_exists(self, cc):
        pass
    def test_var_a(self, cc):
        assert hasattr(cc, "a")
    def test_a_val(self, cc):
        assert cc.a == "coffee"
    def test_var_b(self, cc):
        assert hasattr(cc, "b")
    def test_b_val(self, cc):
        assert cc.b == "cake"        
    def test_func1_exists(self, cc):
        assert hasattr(cc, "func1")
    def test_func1_output(self, cc):
        assert cc.func1() == ("drunk", "eaten")
    def test_func2_exists(self, cc):
        assert hasattr(cc, "func2")
    def test_func2_output(self, cc):
        assert cc.func2(1, 2) == ("drunk", "eaten")
    def test_func3_exists(self, cc):
        assert hasattr(cc, "func3")
    def test_func3_output(self, cc):
        assert cc.func3() == "coffee"
        assert cc.func3() is cc.a
    def test_func4_exists(self, cc):
        assert hasattr(cc, "func4")
    def test_func4_output(self, cc):
        a, b = cc.func4()
        assert (a, b) == ("drunk", "eaten")
        assert a is cc.a

class TestTask11:
    def test_func5_exists(self, cc):
        assert hasattr(cc, "func5")

    def test_func5_output_type(self, cc):
        assert isinstance(cc.func5(), dict)

    def test_func5_output(self, cc):
        assert cc.func5()['a'] == "drunk"

    def test_func6_exists(self, cc):
        assert hasattr(cc, "func6")

    def test_func6_output_type(self, cc):
        assert isinstance(cc.func6(), dict)

    def test_func6_output(self, cc):
        assert cc.func6()['a'] != "empty"
