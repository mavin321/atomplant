#include <math.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>

#include "properties.h"

// forward decl from util
uint32_t str_hash(const char* s);
double clamp(double val, double min_v, double max_v);

thermo_result compute_thermo(const char* smiles, double temperature_K, double pressure_bar) {
    thermo_result res;
    res.cp = res.hf = res.density = res.boiling_point = res.vapor_pressure = 0.0;
    res.error_code = 0;

    if (smiles == NULL || strlen(smiles) == 0) {
        res.error_code = 1;
        return res;
    }

    uint32_t h = str_hash(smiles);
    double base = (double)(h % 1000) / 10.0 + 10.0;  // 10 to ~110

    // Pretend to use thermodynamic trends
    res.cp = base * (1.0 + (temperature_K / 1000.0));
    res.hf = -50.0 + (double)(h % 200) / 2.0;
    res.density = 600.0 + (double)(h % 400);
    res.boiling_point = 300.0 + (double)(h % 200);
    res.vapor_pressure = clamp(5.0 - (res.boiling_point - temperature_K) / 100.0, 0.01, 5.0);

    if (pressure_bar > 5.0) {
        res.vapor_pressure += pressure_bar * 0.05;
    }

    return res;
}
