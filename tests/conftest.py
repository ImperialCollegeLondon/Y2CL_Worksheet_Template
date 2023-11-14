from importlib import import_module
from types import FunctionType
import pytest

@pytest.fixture(scope="module")
def sh():
    return import_module("shapes")

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
def re_namespace(sh):
    if "Rectangle" not in vars(sh):
        return {}
    return vars(sh.Rectangle)
@pytest.fixture
def tr_namespace(sh):
    if "Triangle" not in vars(sh):
        return {}
    return vars(sh.Triangle)
@pytest.fixture
def el_namespace(sh):
    if "Ellipse" not in vars(sh):
        return {}
    return vars(sh.Ellipse)

@pytest.fixture
def rectangle(sh):
    sh1 = sh.Rectangle(12, 11)
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
def ellipse(sh):
    sh1 = sh.Ellipse(5., 6.)
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

@pytest.fixture()
def vh():
    return import_module("vehicles")

@pytest.fixture
def en_namespace(vh):
    if "Engine" not in vars(vh):
        return {}
    return vars(vh.Engine)

@pytest.fixture
def ca_namespace(vh):
    if "Car" not in vars(vh):
        return {}
    return vars(vh.Car)

@pytest.fixture
def trns_namespace(vh):
    if "Transmission" not in vars(vh):
        return {}
    return vars(vh.Transmission)
