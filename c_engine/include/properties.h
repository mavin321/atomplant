#ifndef PROPERTIES_H
#define PROPERTIES_H

typedef struct {
    double cp;
    double hf;
    double density;
    double boiling_point;
    double vapor_pressure;
    int error_code;
} thermo_result;

thermo_result compute_thermo(const char* smiles, double temperature_K, double pressure_bar);
double estimate_heat_transfer_coeff(double scale_factor, double viscosity, double density);
double estimate_mass_transfer_coeff(double scale_factor, double diffusion_coeff);

#endif
