from importlib import import_module
import pytest
import numpy as np

@pytest.fixture(scope="module")
def mm():
    return import_module("src.mymodule")

class TestTask7:
    def test_module_exists(self, mm):
        pass

class TestTask8:
    def test_import_np(self, mm):
        assert hasattr(mm, "_np")

    def test_sqrt5_present(self, mm):
        assert hasattr(mm, "_sqrt5")

    def test_phi_present(self, mm):
        assert hasattr(mm, "_phi")

    def test_fibo_exists(self, mm):
        assert hasattr(mm, "fibo")

    def test_fibo_output(self, mm):
        assert np.isclose(mm.fibo(5), 5)

    def test_fibo1_exists(self, mm):
        assert hasattr(mm, "fibo1")

    def test_fibo1_output(self, mm):
        assert np.isclose(mm.fibo1(5), 5)

    def test_fibo2_exists(self, mm):
        assert hasattr(mm, "fibo2")

    def test_fibo2_output(self, mm):
        assert np.isclose(mm.fibo2(5), 5)
