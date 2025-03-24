from inspect import signature
import random
import numpy as np


class TestTask24:
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
        assert colour == "Black"

    def test_setter(self, sh_black):
        sh_black.set("Green")
        assert sh_black.colour() == "Green"

    def test_chaining(self, sh, sh_black):
        sh1 = sh_black.set("Green")

        assert isinstance(sh1, sh.Shape)
        assert sh1 is sh_black

class TestTask25:
    def test_rectangle_exists(self, sh):
        assert "Rectangle" in vars(sh), "Missing Rectangle derived class."
    def test_rectangle_inheritance(self, sh):
        assert sh.Shape in sh.Rectangle.__bases__
        #mro = sh.Square.mro()
        #assert len(mro) == 3
        #assert issubclass(mro[1], sh.Shape), "Square should inherit from Shape"
    def test_rectangle_init_method_present(self, re_namespace):
        assert "__init__" in re_namespace
    def test_rectangle_area_method_present(self, re_namespace):
        assert "area" in re_namespace
    def test_rectangle_colour_method_absent(self, re_namespace):
        assert "colour" not in re_namespace, "Rectangle should not have a colour method as it should come from the base class Shape"
    def test_rectangle_set_method_absent(self, re_namespace):
        assert "set" not in re_namespace, "Rectangle should not have a set method as it should come from the base class Shape"
    def test_rectangle_area(self, sh):
        a = random.uniform(1., 10.)
        b = random.uniform(1., 10.)
        rect = sh.Rectangle(a, b)
        rect.set("Black")
        assert np.allclose(rect.area(), a * b)
    def test_rectangle_colour(self, rectangle):
        assert hasattr(rectangle, "colour")
        assert isinstance(rectangle.colour(), str)
    def test_rectangle_set(self, rectangle):
        assert hasattr(rectangle, "set")
        rectangle.set("Green")
        assert rectangle.colour() == "Green"
        rectangle.set("Blue")
        assert rectangle.colour() == "Blue"

    def test_triangle_exists(self, sh):
        assert "Triangle" in vars(sh), "Missing Triangle derived class."
    def test_triangle_inheritance(self, sh):
        assert sh.Shape in sh.Triangle.__bases__
        # mro = sh.Triangle.mro()
        # assert len(mro) == 3
        # assert issubclass(mro[1], sh.Shape), "Triangle should inherit from Shape"
    def test_triangle_init_method_present(self, tr_namespace):
        assert "__init__" in tr_namespace
    def test_triangle_area_method_present(self, tr_namespace):
        assert "area" in tr_namespace
    def test_triangle_colour_method_absent(self, tr_namespace):
        assert "colour" not in tr_namespace, "Triangle should not have a colour method as it should come from the base class Shape"
    def test_triangle_set_method_absent(self, tr_namespace):
        assert "set" not in tr_namespace, "Triangle should not have a set method as it should come from the base class Shape"
    def test_triangle_area(self, sh):
        a = random.uniform(1., 10.)
        b = random.uniform(1., 10.)
        tri = sh.Triangle(a, b)
        tri.set("Black")
        assert np.isclose(tri.area(), 0.5 * a * b)
    def test_triangle_colour(self, triangle):
        assert hasattr(triangle, "colour")
        assert isinstance(triangle.colour(), str)
    def test_triangle_set(self, triangle):
        assert hasattr(triangle, "set")
        triangle.set("Green")
        assert triangle.colour() == "Green"
        triangle.set("Blue")
        assert triangle.colour() == "Blue"

    def test_ellipse_exists(self, sh):
        assert "Ellipse" in vars(sh), "Missing Circle derived class."
    def test_ellipse_inheritance(self, sh):
        assert sh.Shape in sh.Ellipse.__bases__
        # mro = sh.Ellipse.mro()
        # assert len(mro) == 3
        # assert issubclass(mro[1], sh.Shape), "Circle should inherit from Shape"
    def test_ellipse_init_method_present(self, el_namespace):
        assert "__init__" in el_namespace
    def test_circle_area_method_present(self, el_namespace):
        assert "area" in el_namespace
    def test_ellipse_colour_method_absent(self, el_namespace):
        assert "colour" not in el_namespace, "Circle should not have a colour method as it should come from the base class Shape"
    def test_ellipse_set_method_absent(self, el_namespace):
        assert "set" not in el_namespace, "Circle should not have a set method as it should come from the base class Shape"
    def test_ellipse_area(self, sh):
        a = random.uniform(1., 10.)
        b = random.uniform(1., 10.)
        ell = sh.Ellipse(a, b)
        ell.set("Black")
        assert np.isclose(ell.area(), np.pi * a * b)
    def test_ellipse_colour(self, ellipse):
        assert hasattr(ellipse, "colour")
        assert isinstance(ellipse.colour(), str)
    def test_ellipse_set(self, ellipse):
        assert hasattr(ellipse, "colour")
        ellipse.set("Green")
        assert ellipse.colour() == "Green"
        ellipse.set("Blue")
        assert ellipse.colour() == "Blue"


class TestTask27:
    def test_function_exists(self, sh_funcs):
        assert len(sh_funcs) != 0, "Missing function to make Shapes Red."
        assert len(sh_funcs) == 1, "Too many functions to determine which makes Shapes Red"

    def test_make_shape_red(self, red_func, sh_black, rectangle, triangle, ellipse):
        rectangle.set("Black")
        triangle.set("Black")
        ellipse.set("Black")
        correct = ("Red", "red")
        assert sh_black.colour() not in correct
        assert rectangle.colour() not in correct
        assert triangle.colour() not in correct
        assert ellipse.colour() not in correct

        red_func(sh_black)
        red_func(rectangle)
        red_func(triangle)
        red_func(ellipse)
        assert sh_black.colour() in correct
        assert rectangle.colour() in correct
        assert triangle.colour() in correct
        assert ellipse.colour() in correct

    def test_ignore_non_shapes(self, red_func):
        assert red_func(12) == 12
        assert red_func([1., 2., 3.]) == [1., 2., 3.]


class TestTask28:
    def test_counter_exists(self, sh_namespace):
        assert "num_red" in sh_namespace
    def test_zero_initial_count(self, sh):
        assert sh.Shape.num_red == 0
    def test_construction_doesnt_set(self, sh):
        sh1 = sh.Shape("Black")
        assert sh.Shape.num_red == 0
        del sh1
    def test_construction_sets(self, sh):
        assert sh.Shape.num_red == 0
        sh1 = sh.Shape("Red")
        assert sh.Shape.num_red == 1
        sh1.set("Black")  # make sure it's not incremented for next test. Could have decremented in __del__ destructor instead.
        del sh1
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
        del sh1
    def test_rectangle_counter_absent(self, re_namespace):
        assert "num_red" not in re_namespace
    def test_triangle_counter_absent(self, tr_namespace):
        assert "num_red" not in tr_namespace
    def test_ellipse_counter_absent(self, el_namespace):
        assert "num_red" not in el_namespace

    def test_square_set_increment(self, sh, rectangle):
        assert sh.Shape.num_red == 0
        rectangle.set("Red")
        assert sh.Shape.num_red == 1
    def test_rectangle_set_decrement(self, sh, rectangle):
        assert sh.Shape.num_red == 0
        rectangle.set("Red")
        assert sh.Shape.num_red == 1
        rectangle.set("Green")
        assert sh.Shape.num_red == 0
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
    def test_circle_set_increment(self, sh, ellipse):
        assert sh.Shape.num_red == 0
        ellipse.set("Red")
        assert sh.Shape.num_red == 1
    def test_circle_set_decrement(self, sh, ellipse):
        assert sh.Shape.num_red == 0
        ellipse.set("Red")
        assert sh.Shape.num_red == 1
        ellipse.set("Green")
        assert sh.Shape.num_red == 0


class TestTask29:
    def test_eqtriangle_exists(self, sh):
        assert "EquilateralTriangle" in vars(sh)

    def test_eqtriangle_single_param(self, sh):
        assert len(signature(sh.EquilateralTriangle).parameters) == 2

    def test_square_exists(self, sh):
        assert "Square" in vars(sh)

    def test_square_single_param(self, sh):
        assert len(signature(sh.Square).parameters) == 2

    def test_circle_exists(self, sh):
        assert "Circle" in vars(sh)

    def test_circle_single_param(self, sh):
        assert len(signature(sh.Circle).parameters) == 2
