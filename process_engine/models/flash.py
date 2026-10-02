from __future__ import annotations

from typing import List, Tuple

import numpy as np


def cubic_roots(coefficients: List[float]) -> List[float]:
    # Solve a cubic using NumPy's polynomial root utility.
    coefficients = np.asarray(coefficients, dtype=float)
    roots = np.roots(coefficients)
    real_roots = []
    for root in roots:
        if abs(root.imag) < 1e-8:
            real_roots.append(float(root.real))
    return sorted(real_roots)


class PengRobinsonEOS:
    """A compact Peng-Robinson implementation for pure components and idealized mixtures."""

    R = 8.31446261815324

    @staticmethod
    def alpha_factor(temperature: float, critical_temperature: float, acentric_factor: float) -> float:
        kappa = 0.37464 + 1.54226 * acentric_factor - 0.26992 * acentric_factor**2
        return (1.0 + kappa * (1.0 - np.sqrt(temperature / critical_temperature))) ** 2

    @staticmethod
    def pure_compressibility_factor(
        temperature: float,
        pressure: float,
        critical_temperature: float,
        critical_pressure: float,
        acentric_factor: float,
    ) -> float:
        if temperature <= 0 or pressure <= 0:
            raise ValueError("Temperature and pressure must be positive.")
        if critical_temperature <= 0 or critical_pressure <= 0:
            raise ValueError("Critical properties must be positive.")

        a = 0.45724 * PengRobinsonEOS.R**2 * critical_temperature**2 / critical_pressure
        b = 0.07780 * PengRobinsonEOS.R * critical_temperature / critical_pressure
        alpha = PengRobinsonEOS.alpha_factor(temperature, critical_temperature, acentric_factor)
        a *= alpha

        A = a * pressure / (PengRobinsonEOS.R**2 * temperature**2)
        B = b * pressure / (PengRobinsonEOS.R * temperature)

        coefficients = [1.0, -(1.0 + B), A - 3.0 * B**2 - 2.0 * B, -(A * B - B**2 - B**3)]
        roots = cubic_roots(coefficients)
        positive_roots = [value for value in roots if value > 0]
        if not positive_roots:
            raise ValueError("No positive compressibility root was found.")

        # Pick the physically relevant root (largest positive root for vapor phase, smallest for liquid phase).
        return max(positive_roots)

    @staticmethod
    def mixture_compressibility_factor(
        temperature: float,
        pressure: float,
        critical_temperature: dict,
        critical_pressure: dict,
        acentric_factor: dict,
        composition: dict,
    ) -> float:
        if not composition:
            raise ValueError("Composition cannot be empty.")

        total_moles = sum(composition.values())
        if total_moles <= 0:
            raise ValueError("Total composition must be positive.")

        a_mix = 0.0
        b_mix = 0.0
        for name, xi in composition.items():
            if xi <= 0:
                continue
            tc = critical_temperature[name]
            pc = critical_pressure[name]
            w = acentric_factor.get(name, 0.0)
            a_i = 0.45724 * PengRobinsonEOS.R**2 * tc**2 / pc
            b_i = 0.07780 * PengRobinsonEOS.R * tc / pc
            alpha_i = PengRobinsonEOS.alpha_factor(temperature, tc, w)
            a_i *= alpha_i
            a_mix += xi * np.sqrt(a_i) * xi * np.sqrt(a_i)
            b_mix += xi * b_i

        A = a_mix * pressure / (PengRobinsonEOS.R**2 * temperature**2)
        B = b_mix * pressure / (PengRobinsonEOS.R * temperature)

        coefficients = [1.0, -(1.0 + B), A - 3.0 * B**2 - 2.0 * B, -(A * B - B**2 - B**3)]
        roots = cubic_roots(coefficients)
        positive_roots = [value for value in roots if value > 0]
        if not positive_roots:
            raise ValueError("No positive mixture compressibility root was found.")
        return max(positive_roots)
