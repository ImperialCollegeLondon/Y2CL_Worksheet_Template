from importlib import import_module
import pytest
import numpy as np

# pylint: disable=redefined-outer-name

@pytest.fixture(scope="module")
def rel():
    return import_module("src.relativity")

@pytest.fixture
def fv_namespace(rel):
    if "FourVector" not in vars(rel):
        return {}
    return vars(rel.FourVector)

@pytest.fixture()
def fv_default(rel):
    return rel.FourVector()

@pytest.fixture()
def fv_keyword(rel):
    return rel.FourVector(ct=99.9, r=[1.0, 2.0, 3.0])


class TestTask13:
    def test_FourVector_exists(self, rel):
        assert "FourVector" in vars(rel), "Class FourVector missing from relativity module."

    def test_FourVector_docstring(self, rel):
        assert rel.FourVector.__doc__ is not None, "FourVector class is missing a docstring"
        assert rel.FourVector.__doc__ != "", "FourVector class has an empty docstring"

    def test_Fourvector_attributes(self, rel):
        fv1 = rel.FourVector()
        namespace = vars(fv1)
        spacelike_vars = {'r', '_r', '_FourVector__r'}.intersection(namespace)
        timelike_vars = {'ct', '_ct', '_FourVector__ct'}.intersection(namespace)

        assert len(spacelike_vars) != 0, "Spacelike component should be stored in a variable with name r"
        assert len(timelike_vars) != 0, "Timelike component should be stored in a variable with name ct"

        assert len(spacelike_vars) == 1, f"Duplication of spacelike variables {spacelike_vars!s}"
        assert len(timelike_vars) == 1, f"Duplication of timelike variables {timelike_vars!s}"

        spacelike_var, = spacelike_vars
        timelike_var,  = timelike_vars
        spacelike_value = getattr(fv1, spacelike_var)
        timelike_value = getattr(fv1, timelike_var)
        assert isinstance(timelike_value, float), "timelike attribute ct should be of type float"
        assert isinstance(spacelike_value, np.ndarray), "spacelike attribute r should be of type numpy.ndarray"

    def test_default_construction(self, rel):
        fv1 = rel.FourVector()
        namespace = vars(fv1)
        spacelike_vars = {'r', '_r', '_FourVector__r'}.intersection(namespace)
        timelike_vars = {'ct', '_ct', '_FourVector__ct'}.intersection(namespace)
        spacelike_var, = spacelike_vars
        timelike_var,  = timelike_vars

        spacelike_value = getattr(fv1, spacelike_var)
        timelike_value = getattr(fv1, timelike_var)
        assert isinstance(timelike_value, float)
        assert isinstance(spacelike_value, np.ndarray)

        assert np.all(spacelike_value == np.array([0., 0., 0.])),\
                        "Default constructed Fourvector should have spacelike threevector initialised "\
                        f"to origin not {spacelike_value}"
        assert timelike_value == 0.,\
                         "Default constructed Fourvector should have timelike value initialised to "\
                         f"zero not {timelike_value}"

    def test_keyword_construction(self, rel):
        fv2 = rel.FourVector(ct=99.9, r=[1.0, 2.0, 3.0])
        namespace = vars(fv2)
        spacelike_vars = {'r', '_r', '_FourVector__r'}.intersection(namespace)
        timelike_vars = {'ct', '_ct', '_FourVector__ct'}.intersection(namespace)
        spacelike_var, = spacelike_vars
        timelike_var,  = timelike_vars
        spacelike_value = getattr(fv2, spacelike_var)
        timelike_value = getattr(fv2, timelike_var)

        assert isinstance(timelike_value, float)
        assert isinstance(spacelike_value, np.ndarray)


        assert np.all(spacelike_value == np.array([1., 2., 3.])), f"Fourvector spacelike attribute not set correctly; expected [1,2,3], got {spacelike_value!s}"
        assert timelike_value == 99.9, f"Fourvector timelike attribute not set correctly; expected 99.9, got {timelike_value!r}"

    def test_object_independence(self, fv_default, fv_keyword):
        assert fv_default is not fv_keyword, "Should be possible to create independent objcets from your class"

class TestTask14:
    def test_str(self, fv_keyword):
        assert str(fv_keyword) in ["(99.9, 1.0, 2.0, 3.0)", "(99.9, 1., 2., 3.)", "(99.9, 1, 2, 3)"]
    def test_repr(self, fv_keyword):
        assert repr(fv_keyword) in ["FourVector(ct=99.9, r=array([1.0, 2.0, 3.0]))",
                                    "FourVector(ct=99.9, r=array([1., 2., 3.]))",
                                    "FourVector(ct=99.9, r=array([1, 2, 3]))"]

class TestTask15:
    def test_ct_method_present(self, fv_namespace):
        assert "ct" in fv_namespace, "Accessor (getter) method for timelike attribute missing"

    def test_r_method_present(self, fv_namespace):
        assert "r" in fv_namespace, "Accessor (getter) method for spacelike attribute missing"

    def test_setct_method_present(self, fv_namespace):
        assert "setct" in fv_namespace, "modifier (setter) method for timelike attribute missing"

    def test_setr_method_present(self, fv_namespace):
        assert "setr" in fv_namespace, "modifier (setter) method for spacelike attribute missing"

    def test_getters(self, fv_keyword):
        assert isinstance(fv_keyword.ct(), float)
        assert isinstance(fv_keyword.r(), np.ndarray)

        assert fv_keyword.ct() == 99.9
        assert np.all(fv_keyword.r() == np.array([1., 2., 3.]))

    def test_setters(self, fv_keyword):
        fv_keyword.setct(100.1)
        fv_keyword.setr([5, 6, 7])
        assert isinstance(fv_keyword.ct(), float)
        assert isinstance(fv_keyword.r(), np.ndarray)

        assert fv_keyword.ct() == 100.1
        assert np.all(fv_keyword.r() == np.array([5., 6., 7.]))

    def test_hidden_attributed(self, fv_default):
        namespace = vars(fv_default)
        spacelike_vars = {'_r', '_FourVector__r'}.intersection(namespace)
        timelike_vars = {'_ct', '_FourVector__ct'}.intersection(namespace)
        assert len(spacelike_vars) != 0, "Spacelike component should be stored in a hidden variable"
        assert len(timelike_vars) != 0, "Timelike component should be stored in a hidden variable"

        spacelike_var, = spacelike_vars
        timelike_var,  = timelike_vars
        spacelike_value = getattr(fv_default, spacelike_var)
        timelike_value = getattr(fv_default, timelike_var)

        assert isinstance(timelike_value, float)
        assert isinstance(spacelike_value, np.ndarray)

class TestTask16:
    def test_copy_method_present(self, fv_namespace):
        assert "copy" in fv_namespace, "Missing copy method."

    def test_identity(self, fv_keyword):
        fv_new = fv_keyword.copy()
        assert fv_new is not fv_keyword, "Copy is not an independent object."

    def test_equality(self, fv_keyword):
        fv_new = fv_keyword.copy()
        assert fv_new.ct() == fv_keyword.ct(), "Timelike component not copied properly"
        assert np.all(fv_new.r() == fv_keyword.r()), "Spacelike component not copied properly"

class TestTask17:
    def test_add_method_present(self, fv_namespace):
        assert "__add__" in fv_namespace, "Missing __add__ method."
    def test_iadd_method_present(self, fv_namespace):
        assert "__iadd__" in fv_namespace, "Missing __iadd__ method."
    def test_sub_method_present(self, fv_namespace):
        assert "__sub__" in fv_namespace, "Missing __sub__ method."
    def test_isub_method_present(self, fv_namespace):
        assert "__isub__" in fv_namespace, "Missing __isub__ method."

    def test_add(self, rel):
        fv1 = rel.FourVector(ct=99, r=[1.0, 2.0, 3.0])
        fv2 = rel.FourVector(ct=100, r=[5.0, 5.0, 5.0])
        assert fv1 is not fv2

        fv3 = fv1 + fv2
        assert fv3 is not fv1
        assert fv3 is not fv2
        assert fv3.ct() == 199.0
        assert np.all(fv3.r() == np.array([6., 7., 8.]))

    def test_sub(self, rel):
        fv1 = rel.FourVector(ct=99, r=[1.0, 2.0, 3.0])
        fv2 = rel.FourVector(ct=100, r=[5.0, 5.0, 5.0])
        assert fv1 is not fv2

        fv4 = fv2 - fv1
        assert fv4 is not fv1
        assert fv4 is not fv2
        assert fv4.ct() == 1.0
        assert np.all(fv4.r() == np.array([4., 3., 2.]))

    def test_iadd(self, rel):
        fv1 = rel.FourVector(ct=99, r=[1.0, 2.0, 3.0])
        fv2 = rel.FourVector(ct=100, r=[5.0, 5.0, 5.0])
        assert fv1 is not fv2

        orig_id = id(fv1)
        fv1 += fv2
        assert id(fv1) == orig_id
        assert fv1.ct() == 199.0
        assert np.all(fv1.r() == np.array([6., 7., 8.]))

    def test_isub(self, rel):
        fv1 = rel.FourVector(ct=199.0, r=[6., 7., 8.])
        fv2 = rel.FourVector(ct=100, r=[5.0, 5.0, 5.0])
        assert fv1 is not fv2

        orig_id = id(fv1)
        fv1 -= fv2
        assert id(fv1) == orig_id
        assert fv1.ct() == 99.0
        assert np.all(fv1.r() == np.array([1., 2., 3.]))

class TestTask18:
    def test_inner_method_present(self, fv_namespace):
        assert "inner" in fv_namespace, "Missing inner method."
    def test_magsquare_method_present(self, fv_namespace):
        assert "magsquare" in fv_namespace, "Missing magsquare method."
    def test_inner(self, rel):
        fv1 = rel.FourVector(ct=99, r=[1.0, 2.0, 3.0])
        fv2 = rel.FourVector(ct=100, r=[5.0, 5.0, 5.0])
        assert fv1.inner(fv2) == 9870.0
    def test_magsquare(self, rel):
        fv1 = rel.FourVector(ct=99, r=[1.0, 2.0, 3.0])
        assert fv1.magsquare() == 9787.0
        assert fv1.magsquare() == fv1.inner(fv1)

class TestTask19:
    def test_boost_method_present(self, fv_namespace):
        assert "boost" in fv_namespace, "Missing boost method."

    def test_magsquare(self, rel):
        fv1 = rel.FourVector(ct=99, r=[1.0, 2.0, 3.0])
        assert fv1.magsquare() == 9787.0
        fv2 = fv1.boost(0.5)
        assert np.isclose(fv2.magsquare(), 9787.0)

class TestTask20:
    def test_too_many_dims(self, rel):
        with pytest.raises(Exception):
            rel.FourVector(ct=99, r=[1.0, 2.0, 3.0, 4.0])
    def test_too_few_dims(self, rel):
        with pytest.raises(Exception):
            rel.FourVector(ct=99, r=[1.0, 2.0])
