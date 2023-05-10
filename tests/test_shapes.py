from importlib import import_module
from types import FunctionType
import numpy as np
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


class TestTask21:
    def test_shape_exists(self, sh):
        assert "Shape" in vars(sh), "Missing Shape base class."
    
    def test_hidden_attributes(self, sh):
        sh1 = sh.Shape("Black")
        instance_namespace = vars(sh1)
        assert len({'_colour', '_Shape__colour'}.intersection(instance_namespace)) != 0, "Shape class needs a colour attribute that should be hidden."

    def test_colour_method_present(self, sh_namespace):
        assert "colour" in sh_namespace
    def test_set_method_present(self, sh_namespace):
        assert "set" in sh_namespace

    def test_getter(self, sh_black):
        colour = sh_black.colour()
        assert isinstance(colour, str), "accessor method colour should return a string"
        assert colour, "Black"

    def test_setter(self, sh_black):
        sh_black.set("Green")
        assert sh_black.colour() == "Green"

    def test_chaining(self, sh, sh_black):
        sh1 = sh_black.set("Green")

        assert isinstance(sh1, sh.Shape)
        assert sh1 is sh_black

class TestTask22:
    def test_square_exists(self, sh):
        assert "Square" in vars(sh), "Missing Square derived class."
    def test_square_inheritance(self, sh):
        assert sh.Shape in sh.Square.__bases__
        #mro = sh.Square.mro()
        #assert len(mro) == 3
        #assert issubclass(mro[1], sh.Shape), "Square should inherit from Shape"
    def test_square_init_method_present(self, sq_namespace):
        assert "__init__" in sq_namespace
    def test_square_area_method_present(self, sq_namespace):
        assert "area" in sq_namespace
    def test_square_colour_method_absent(self, sq_namespace):
        assert "colour" not in sq_namespace, "Square should not have a colour method as it should come from the base class Shape"
    def test_square_set_method_absent(self, sq_namespace):
        assert "set" not in sq_namespace, "Square should not have a set method as it should come from the base class Shape"
    def test_square_area(self, square):
        assert square.area() == 144
    def test_square_colour(self, square):
        assert hasattr(square, "colour")
        assert isinstance(square.colour(), str)
    def test_square_set(self, square):
        assert hasattr(square, "set")
        square.set("Green")
        assert square.colour() == "Green"
        square.set("Blue")
        assert square.colour() == "Blue"

    def test_triangle_exists(self, sh):
        assert "Triangle" in vars(sh), "Missing Triangle derived class."
    def test_triangle_inheritance(self, sh):
        mro = sh.Triangle.mro()
        assert len(mro) == 3
        assert issubclass(mro[1], sh.Shape), "Triangle should inherit from Shape"
    def test_triangle_init_method_present(self, tr_namespace):
        assert "__init__" in tr_namespace
    def test_triangle_area_method_present(self, tr_namespace):
        assert "area" in tr_namespace
    def test_triangle_colour_method_absent(self, tr_namespace):
        assert "colour" not in tr_namespace, "Triangle should not have a colour method as it should come from the base class Shape"
    def test_triangle_set_method_absent(self, tr_namespace):
        assert "set" not in tr_namespace, "Triangle should not have a set method as it should come from the base class Shape"
    def test_triangle_area(self, triangle):
        assert triangle.area() == 30.
    def test_triangle_colour(self, triangle):
        assert hasattr(triangle, "colour")
        assert isinstance(triangle.colour(), str)
    def test_triangle_set(self, triangle):
        assert hasattr(triangle, "set")
        triangle.set("Green")
        assert triangle.colour() == "Green"
        triangle.set("Blue")
        assert triangle.colour() == "Blue"

    def test_circle_exists(self, sh):
        assert "Circle" in vars(sh), "Missing Circle derived class."
    def test_circle_inheritance(self, sh):
        mro = sh.Circle.mro()
        assert len(mro) == 3
        assert issubclass(mro[1], sh.Shape), "Circle should inherit from Shape"
    def test_circle_init_method_present(self, ci_namespace):
        assert "__init__" in ci_namespace
    def test_circle_area_method_present(self, ci_namespace):
        assert "area" in ci_namespace
    def test_circle_colour_method_absent(self, ci_namespace):
        assert "colour" not in ci_namespace, "Circle should not have a colour method as it should come from the base class Shape"
    def test_circle_set_method_absent(self, ci_namespace):
        assert "set" not in ci_namespace, "Circle should not have a set method as it should come from the base class Shape"
    def test_circle_area(self, circle):
        assert circle.area() == np.pi * 25.
    def test_circle_colour(self, circle):
        assert hasattr(circle, "colour")
        assert isinstance(circle.colour(), str)
    def test_circle_set(self, circle):
        assert hasattr(circle, "colour")
        circle.set("Green")
        assert circle.colour() == "Green"
        circle.set("Blue")
        assert circle.colour() == "Blue"

class TestTask24:
    def test_function_exists(self, sh_funcs):
        assert len(sh_funcs) != 0, "Missing function to make Shapes Red."
        assert len(sh_funcs) == 1, "Too many functions to determine which makes Shapes Red"

    def test_make_shape_red(self, red_func, sh_black, square, triangle, circle):
        square.set("Black")
        triangle.set("Black")
        circle.set("Black")
        correct = ("Red", "red")
        assert sh_black.colour() not in correct
        assert square.colour() not in correct
        assert triangle.colour() not in correct
        assert circle.colour() not in correct

        red_func(sh_black)
        red_func(square)
        red_func(triangle)
        red_func(circle)
        assert sh_black.colour() in correct
        assert square.colour() in correct
        assert triangle.colour() in correct
        assert circle.colour() in correct
    def test_ignore_non_shapes(self, red_func):
        assert red_func(12) == 12
        assert red_func([1., 2., 3.]) == [1., 2., 3.]

class TestTask25:
    def test_counter_exists(self, sh_namespace):
        assert "num_red" in sh_namespace
    def test_zero_initial_count(self, sh):
        assert sh.Shape.num_red == 0
    def test_construction_doesnt_set(self, sh):
        sh.Shape("Black")
        assert sh.Shape.num_red == 0
    def test_construction_sets(self, sh):
        assert sh.Shape.num_red == 0
        sh1 = sh.Shape("Red")
        assert sh.Shape.num_red == 1
        sh1.set("Black")  # make sure it's not incremented for next test. Could have decremented in __del__ destructor instead.
    def test_set_increments(self, sh, sh_black):
        assert sh.Shape.num_red == 0
        sh_black.set("Red")
        assert sh.Shape.num_red == 1
    def test_set_decrements(self, sh):
        assert sh.Shape.num_red == 0
        sh1 = sh.Shape("Red")
        assert sh.Shape.num_red == 1
        sh1.set("Black")
        assert sh.Shape.num_red == 0

    def test_square_counter_absent(self, sq_namespace):
        assert "num_red" not in sq_namespace
    def test_triangle_counter_absent(self, tr_namespace):
        assert "num_red" not in tr_namespace
    def test_circle_counter_absent(self, ci_namespace):
        assert "num_red" not in ci_namespace

    def test_square_set_increment(self, sh, square):
        assert sh.Square.num_red == 0
        square.set("Red")
        assert sh.Square.num_red == 1
    def test_square_set_decrement(self, sh, square):
        assert sh.Square.num_red == 0
        square.set("Red")
        assert sh.Square.num_red == 1
        square.set("Green")
        assert sh.Square.num_red == 0
    def test_triangle_set_increment(self, sh, triangle):
        assert sh.Triangle.num_red == 0
        triangle.set("Red")
        assert sh.Triangle.num_red == 1
    def test_triangle_set_decrement(self, sh, triangle):
        assert sh.Triangle.num_red == 0
        triangle.set("Red")
        assert sh.Triangle.num_red == 1
        triangle.set("Green")
        assert sh.Triangle.num_red == 0
    def test_circle_set_increment(self, sh, circle):
        assert sh.Circle.num_red == 0
        circle.set("Red")
        assert sh.Circle.num_red == 1
    def test_circle_set_decrement(self, sh, circle):
        assert sh.Circle.num_red == 0
        circle.set("Red")
        assert sh.Circle.num_red == 1
        circle.set("Green")
        assert sh.Circle.num_red == 0
