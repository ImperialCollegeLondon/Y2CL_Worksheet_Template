from importlib import import_module
from types import FunctionType
import pytest

# @pytest.fixture(scope="module")
# def sh():
#     return import_module("shapes1")

@pytest.fixture
def sh_namespace(sh):
    if "Shape" not in vars(sh):
        return {}
    return vars(sh.Shape)

@pytest.fixture
def sh_black(sh):
    sh1 = sh.Shape("Black")
    yield sh1  # incase the default has been set to red. This would mess up the counting tests.
    sh1.set("Black")

@pytest.fixture
def sq_namespace(sh):
    if "Square" not in vars(sh):
        return {}
    return vars(sh.Square)
@pytest.fixture
def tr_namespace(sh):
    if "Triangle" not in vars(sh):
        return {}
    return vars(sh.Triangle)
@pytest.fixture
def ci_namespace(sh):
    if "Circle" not in vars(sh):
        return {}
    return vars(sh.Circle)

@pytest.fixture
def square(sh):
    sh1 = sh.Square(12)
    sh1.set("Black")  # incase the default has been set to red. This would mess up the counting tests.
    yield sh1
    sh1.set("Black")

@pytest.fixture
def triangle(sh):
    sh1 = sh.Triangle(12, 5)
    sh1.set("Black")  # incase the default has been set to red. This would mess up the counting tests.
    yield sh1
    sh1.set("Black")

@pytest.fixture
def circle(sh):
    sh1 = sh.Circle(5.)
    sh1.set("Black")  # incase the default has been set to red. This would mess up the counting tests.
    yield sh1
    sh1.set("Black")

@pytest.fixture
def sh_funcs(sh):
    return {k: v for k, v in vars(sh).items() if isinstance(v, FunctionType)}

@pytest.fixture
def red_func(sh_funcs):
    assert len(sh_funcs) == 1
    _, red_func = list(sh_funcs.items())[0]
    return red_func
