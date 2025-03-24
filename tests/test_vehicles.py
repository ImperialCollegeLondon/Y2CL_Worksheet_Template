"""Test for vehicles module."""
import sys
from io import StringIO
from inspect import signature
from unittest.mock import MagicMock
import pytest

class TestTask21:
    def test_vehicles_exists(self, vh):
        pass

    def test_engine_exists(self, vh):
        assert "Engine" in vars(vh), "Missing Engine class."

    def test_engine_init_exists(self, en_namespace):
        assert "__init__" in en_namespace

    def test_engine_construction(self, vh):
        vh.Engine("petrol")

    def test_engine_start_present(self, en_namespace):
        assert "start" in en_namespace

    def test_engine_start_prints(self, vh):
        stdout_buff = StringIO()
        sys.stdout, tmp_stdout = stdout_buff, sys.stdout
        e = vh.Engine("petrol")
        assert e.start() is None
        assert sys.stdout.getvalue(), "Expected some printout."
        sys.stdout = tmp_stdout


class TestTask22:
    def test_car_exists(self, vh):
        assert "Car" in vars(vh), "Missing Car class."

    def test_car_construction(self, vh):
        nparams = len(signature(vh.Car).parameters)
        assert nparams in (1, 2), "Unusual number of parameters to Car __init__ method."
        if nparams == 1:
            vh.Car(engine=vh.Engine("petrol"))
        elif nparams == 2:
            assert "Transmission" in vars(vh)
            vh.Car(engine=vh.Engine("petrol"), transmission=vh.Transmission("automatic", 5))

    def test_car_start_present(self, ca_namespace):
        assert "start" in ca_namespace

    def test_car_calls_engine(self, vh, monkeypatch):
        start_mock = MagicMock()
        monkeypatch.setattr(vh.Engine, "start", start_mock)

        nparams = len(signature(vh.Car).parameters)
        if nparams == 1:
            c = vh.Car(engine=vh.Engine("petrol"))
        elif nparams == 2:
            assert "Transmission" in vars(vh)
            c = vh.Car(engine=vh.Engine("petrol"), transmission=vh.Transmission("automatic", 5))
        c.start()
        start_mock.assert_called_once()

    def test_car_start_prints(self, vh):
        nparams = len(signature(vh.Car).parameters)
        stdout_buff = StringIO()
        sys.stdout, tmp_stdout = stdout_buff, sys.stdout        
        assert nparams in (1, 2), "Unusual number of parameters to Car __init__ method."
        if nparams == 1:
            c = vh.Car(engine=vh.Engine("petrol"))
        elif nparams == 2:
            assert "Transmission" in vars(vh)
            c = vh.Car(engine=vh.Engine("petrol"), transmission=vh.Transmission("automatic", 5))
        assert c.start() is None
        assert len(sys.stdout.getvalue().splitlines()) == 2, "Expected printout from both Engine and Car start methods."
        sys.stdout = tmp_stdout


class TestTask23:
    def test_transmission_exists(self, vh):
        assert "Transmission" in vars(vh)

    def test_transmission_construction(self, vh):
        vh.Transmission("manual", 5)

    def test_type_method_exists(self, trns_namespace):
        assert "type" in trns_namespace

    def test_type_return(self, vh):
        trans1 = vh.Transmission("manual", 5)
        assert trans1.type() == "manual"

        trans2 = vh.Transmission("automatic", 5)
        assert trans2.type() == "automatic"

    def test_gear_method_exists(self, trns_namespace):
        assert "gear" in trns_namespace

    def test_gear_return(self, vh):
        trans1 = vh.Transmission("manual", 5)
        assert trans1.gear() == 0

    def test_shift_up_exists(self, trns_namespace):
        assert "shift_up" in trns_namespace

    def test_shift_up_implementation(self, vh):
        trans1 = vh.Transmission("manual", 2)
        assert trans1.gear() == 0
        assert trans1.shift_up() in (None, 1)
        assert trans1.gear() == 1
        assert trans1.shift_up() in (None, 2)
        assert trans1.gear() == 2
        assert trans1.shift_up() in (None, 2)
        assert trans1.gear() == 2

        trans2 = vh.Transmission("automatic", 5)
        assert trans2.gear() == 0
        with pytest.raises(Exception):
            trans2.shift_up()

    def test_shift_down_exists(self, trns_namespace):
        assert "shift_down" in trns_namespace

    def test_shift_down_implementation(self, vh):
        trans1 = vh.Transmission("manual", 2)
        assert trans1.gear() == 0
        trans1.shift_up()
        assert trans1.gear() == 1
        assert trans1.shift_down() in (None, 0)
        assert trans1.gear() == 0
        assert trans1.shift_down() in (None, 0)
        assert trans1.gear() == 0        

        trans2 = vh.Transmission("automatic", 5)
        assert trans2.gear() == 0
        with pytest.raises(Exception):
            trans2.shift_down()

    def test_car_shift_up_exists(self, ca_namespace):
        assert "shift_up" in ca_namespace

    def test_car_shift_up_calls(self, vh, monkeypatch):
        sh_up_mock = MagicMock()
        monkeypatch.setattr(vh.Transmission, "shift_up", sh_up_mock)
        c = vh.Car(engine=vh.Engine("petrol"), transmission=vh.Transmission("manual", 5))
        c.shift_up()
        sh_up_mock.assert_called_once()

    def test_car_shift_down(self, ca_namespace):
        assert "shift_down" in ca_namespace

    def test_car_shift_down_calls(self, vh, monkeypatch):
        sh_down_mock = MagicMock()
        monkeypatch.setattr(vh.Transmission, "shift_down", sh_down_mock)
        c = vh.Car(engine=vh.Engine("petrol"), transmission=vh.Transmission("manual", 5))
        c.shift_down()
        sh_down_mock.assert_called_once()

    def test_call_safety_check(self, vh, monkeypatch):
        engine = vh.Engine("petrol")
        manual_trns = vh.Transmission("manual", 5)
        auto_trans = vh.Transmission("automatic", 5)
        gear_4_mock = MagicMock(return_value=4)
        gear_0_mock = MagicMock(return_value=0)

        with monkeypatch.context() as mpc:
            mpc.setattr(vh.Transmission, "gear", gear_0_mock)
            vh.Car(engine=engine, transmission=manual_trns).start()

        with monkeypatch.context() as mpc:
            mpc.setattr(vh.Transmission, "gear", gear_4_mock)
            with pytest.raises(Exception):
                vh.Car(engine=engine, transmission=manual_trns).start()

        with monkeypatch.context() as mpc:
            mpc.setattr(vh.Transmission, "gear", gear_0_mock)
            vh.Car(engine=engine, transmission=auto_trans).start()

        with monkeypatch.context() as mpc:
            mpc.setattr(vh.Transmission, "gear", gear_4_mock)
            vh.Car(engine=engine, transmission=auto_trans).start()
