#include <math.h>
#include <stdint.h>
#include <string.h>

// Simple stable hash for deterministic pseudo-physics numbers.
uint32_t str_hash(const char* s) {
    uint32_t hash = 5381;
    int c;
    while ((c = *s++)) {
        hash = ((hash << 5) + hash) + (uint32_t)c; // hash * 33 + c
    }
    return hash;
}

double clamp(double val, double min_v, double max_v) {
    if (val < min_v) return min_v;
    if (val > max_v) return max_v;
    return val;
}
