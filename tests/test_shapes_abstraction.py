
import inspect as ins
from importlib import import_module, reload
import re
from textwrap import dedent
from inspect import getsource
from unittest.mock import MagicMock
import numpy as np


class TestTask30:
    def test_module_exists(self, sh_ab):
        pass

    def test_shape_in_scope(self, sh_ab):
        assert "Shape" in vars(sh_ab)

    def test_not_reimplemented(self, sh, sh_ab, monkeypatch):
        sh_rel = import_module("src.shapes")
        shape_mock = MagicMock()
        with monkeypatch.context() as mpc:
            mpc.setattr(sh, "Shape", shape_mock)
            mpc.setattr(sh_rel, "Shape", shape_mock)
            reload(sh_ab)
            assert sh_ab.Shape is shape_mock
        reload(sh_ab)

    def test_no_relative_imports(self, sh_ab):
        RELATIVE_IMPORTS_REGEX = re.compile(r"^\s*((?:import|from)\s+[.]?shapes.*?)$", re.MULTILINE)
        relative_imports = RELATIVE_IMPORTS_REGEX.findall(getsource(sh_ab))
        relative_imports_str = f"\n{' '*8}".join(f"{i+1}: {import_line.strip()}" for i, import_line in enumerate(relative_imports))
        msg = dedent(f"""
        {len(relative_imports)} Relative imports found in shapes_abstraction.py:
        {'-'*20}
        {relative_imports_str}
        {'-'*20}
        These should use absolute imports i.e. src.<module>

        """)
        assert not relative_imports, msg


class TestTask31:
    def test_regularpolygon_exists(self, sh_ab):
        assert "RegularPolygon" in vars(sh_ab)

    def test_construction(self, sh_ab):
        sh_ab.RegularPolygon(n_sides=4, side_length=3)
        sh_ab.RegularPolygon(n_sides=3, side_length=4, colour="blue")

    def test_area_present(self, sh_ab):
        assert "area" in vars(sh_ab.RegularPolygon)

    def test_area_calculation(self, sh_ab):
        assert np.isclose(sh_ab.RegularPolygon(n_sides=3, side_length=5).area(), 10.825317547305486)
        assert np.isclose(sh_ab.RegularPolygon(n_sides=4, side_length=5).area(), 25.)
        assert np.isclose(sh_ab.RegularPolygon(n_sides=5, side_length=5).area(), 43.01193501472418)


class TestTask32:
    def test_eqtriangle_exists(self, sh_ab):
        assert "EquilateralTriangle" in vars(sh_ab)

    def test_eqtriangle_construction(self, sh_ab):
        sh_ab.EquilateralTriangle(side_length=5)
        sh_ab.EquilateralTriangle(side_length=5, colour="yellow")

    def test_square_exists(self, sh_ab):
        assert "Square" in vars(sh_ab)

    def test_square_construction(self, sh_ab):
        sh_ab.Square(side_length=5)
        sh_ab.Square(side_length=5, colour="magenta")

    def test_pentagon_exists(self, sh_ab):
        assert "Pentagon" in vars(sh_ab)
    
    def test_pentagon_construction(self, sh_ab):
        sh_ab.Pentagon(side_length=5)
        sh_ab.Pentagon(side_length=5, colour="black")


class TestTask33:
    def test_angles_method_exists(self, sh_ab):
        assert "interior_angle" in vars(sh_ab.RegularPolygon)

    def test_interior_angle(self, sh_ab):
        assert np.isclose(sh_ab.EquilateralTriangle(side_length=5).interior_angle(), 60.)
        assert np.isclose(sh_ab.Square(side_length=5).interior_angle(), 90.)
        assert np.isclose(sh_ab.Pentagon(side_length=5).interior_angle(), 108.)

    def test_tessellate_exists(self, sh_ab):
        assert ("can_tessellate" in vars(sh_ab.RegularPolygon)) or \
            ("can_tessellate" in vars(sh_ab.EquilateralTriangle) and
             "can_tessellate" in vars(sh_ab.Square) and
             "can_tessellate" in vars(sh_ab.Pentagon))
        assert ("can_tessellate" in vars(sh_ab.RegularPolygon)) != \
            ("can_tessellate" in vars(sh_ab.EquilateralTriangle) or
             "can_tessellate" in vars(sh_ab.Square) or 
             "can_tessellate" in vars(sh_ab.Pentagon)), "can_tessellate should not be in both base and derived classes."

    def test_can_tessellate(self, sh_ab):
        assert sh_ab.EquilateralTriangle(side_length=5).can_tessellate()
        assert sh_ab.Square(side_length=5).can_tessellate()
        assert not sh_ab.Pentagon(side_length=5).can_tessellate()
