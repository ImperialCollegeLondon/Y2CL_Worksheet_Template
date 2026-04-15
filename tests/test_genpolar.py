from importlib import import_module
from collections.abc import Generator
from inspect import signature
import numpy as np
import pytest


@pytest.fixture(scope="module")
def genpolar():
    return import_module("src.genpolar")


class TestTask12:

    def test_genpolar_exists(self, genpolar):
        pass

    def test_rtrings_exists(self, genpolar):
        assert hasattr(genpolar, "rtrings")

    def test_rtrings_args(self, genpolar):
        assert not {'nrings', 'rmax', 'multi'}.difference(signature(genpolar.rtrings).parameters.keys())

    def test_generator_type(self, genpolar):
        assert isinstance(genpolar.rtrings(rmax=5., nrings=5, multi=6), Generator)

    def test_rtrings_correct(self, genpolar):
        positions = {(float(np.round(radius, 12)), float(np.round(theta, 12)))
                     for radius, theta in genpolar.rtrings(rmax=5., nrings=5, multi=6)}
        expected_positions = {(0.0, 0.0),
                              (1.0, 0.0),
                              (1.0, 1.047197551197),
                              (1.0, 2.094395102393),
                              (1.0, 3.14159265359),
                              (1.0, 4.188790204786),
                              (1.0, 5.235987755983),
                              (2.0, 0.0),
                              (2.0, 0.523598775598),
                              (2.0, 1.047197551197),
                              (2.0, 1.570796326795),
                              (2.0, 2.094395102393),
                              (2.0, 2.617993877991),
                              (2.0, 3.14159265359),
                              (2.0, 3.665191429188),
                              (2.0, 4.188790204786),
                              (2.0, 4.712388980385),
                              (2.0, 5.235987755983),
                              (2.0, 5.759586531581),
                              (3.0, 0.0),
                              (3.0, 0.349065850399),
                              (3.0, 0.698131700798),
                              (3.0, 1.047197551197),
                              (3.0, 1.396263401595),
                              (3.0, 1.745329251994),
                              (3.0, 2.094395102393),
                              (3.0, 2.443460952792),
                              (3.0, 2.792526803191),
                              (3.0, 3.14159265359),
                              (3.0, 3.490658503989),
                              (3.0, 3.839724354388),
                              (3.0, 4.188790204786),
                              (3.0, 4.537856055185),
                              (3.0, 4.886921905584),
                              (3.0, 5.235987755983),
                              (3.0, 5.585053606382),
                              (3.0, 5.934119456781),
                              (4.0, 0.0),
                              (4.0, 0.261799387799),
                              (4.0, 0.523598775598),
                              (4.0, 0.785398163397),
                              (4.0, 1.047197551197),
                              (4.0, 1.308996938996),
                              (4.0, 1.570796326795),
                              (4.0, 1.832595714594),
                              (4.0, 2.094395102393),
                              (4.0, 2.356194490192),
                              (4.0, 2.617993877991),
                              (4.0, 2.879793265791),
                              (4.0, 3.14159265359),
                              (4.0, 3.403392041389),
                              (4.0, 3.665191429188),
                              (4.0, 3.926990816987),
                              (4.0, 4.188790204786),
                              (4.0, 4.450589592586),
                              (4.0, 4.712388980385),
                              (4.0, 4.974188368184),
                              (4.0, 5.235987755983),
                              (4.0, 5.497787143782),
                              (4.0, 5.759586531581),
                              (4.0, 6.02138591938),
                              (5.0, 0.0),
                              (5.0, 0.209439510239),
                              (5.0, 0.418879020479),
                              (5.0, 0.628318530718),
                              (5.0, 0.837758040957),
                              (5.0, 1.047197551197),
                              (5.0, 1.256637061436),
                              (5.0, 1.466076571675),
                              (5.0, 1.675516081915),
                              (5.0, 1.884955592154),
                              (5.0, 2.094395102393),
                              (5.0, 2.303834612633),
                              (5.0, 2.513274122872),
                              (5.0, 2.722713633111),
                              (5.0, 2.93215314335),
                              (5.0, 3.14159265359),
                              (5.0, 3.351032163829),
                              (5.0, 3.560471674068),
                              (5.0, 3.769911184308),
                              (5.0, 3.979350694547),
                              (5.0, 4.188790204786),
                              (5.0, 4.398229715026),
                              (5.0, 4.607669225265),
                              (5.0, 4.817108735504),
                              (5.0, 5.026548245744),
                              (5.0, 5.235987755983),
                              (5.0, 5.445427266222),
                              (5.0, 5.654866776462),
                              (5.0, 5.864306286701),
                              (5.0, 6.07374579694)}

        npositions = len(positions)
        nexpected_positions = len(expected_positions)
        assert npositions == 91, f"Incorrect number of positions, expected 91, got {npositions}"
        assert nexpected_positions == 91, f"Incorrect number of expectation positions, expected 91, got {nexpected_positions}"

        missing = expected_positions - positions
        extra = positions - expected_positions

        if missing:
            print("Missing expected rows:")
            for row in missing:
                print("   ", row)
        if extra:
            print("Extra unexpected rows:")
            for row in extra:
                print("   ", row)

        n_mismatches = len(missing) + len(extra)
        assert n_mismatches == 0, f"{n_mismatches} Mismatch(es) between actual and expected positions"
