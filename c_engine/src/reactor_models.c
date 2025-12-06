#include "properties.h"

double estimate_heat_transfer_coeff(double scale_factor, double viscosity, double density) {
    // Placeholder using Dittus-Boelter-like scaling
    double base = 150.0 * scale_factor;
    double visc_term = viscosity > 0 ? (1.0 / (1.0 + viscosity)) : 1.0;
    double dens_term = density > 0 ? (density / 1000.0) : 1.0;
    return base * visc_term * dens_term;
}

double estimate_mass_transfer_coeff(double scale_factor, double diffusion_coeff) {
    if (diffusion_coeff <= 0) diffusion_coeff = 1e-9;
    return 0.01 * scale_factor * diffusion_coeff * 1e9;
}
