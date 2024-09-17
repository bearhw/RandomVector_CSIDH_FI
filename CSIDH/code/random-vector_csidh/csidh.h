/*
    This is the header file of dynamic random vector CSIDH functions
    Copyright (C) 2024 Ting Hung Chiu (kennychiu0818@vt.edu)

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
*/
#ifndef CSIDH_H
#define CSIDH_H

#include <stdbool.h>
#include <stddef.h>

#include "params.h"

/* specific to p, should perhaps be somewhere else */
#define num_primes 74
//fp invs_[9];

//const unsigned primes[num_primes];

typedef struct private_key {
    int8_t e[num_primes];
} private_key;

typedef struct public_key {
    fp A; /* Montgomery coefficient: represents y^2 = x^3 + Ax^2 + x */
} public_key;

extern const public_key base;


void csidh_private(private_key *priv, const int8_t *max_exponent);
bool action(public_key *out, public_key const *in, private_key const *priv,
		uint8_t num_intervals, int8_t const *max_exponent, unsigned int const num_isogenies, uint8_t const my,int8_t** vector);
bool csidh(public_key *out, public_key const *in, private_key const *priv,
		uint8_t const num_intervals, int8_t const *max_exponent, unsigned int const num_isogenies, uint8_t const my,int8_t** vector);
void elligator(proj *P, proj *Pd, const fp *A);
bool validate(public_key const *in);



int32_t lookup(size_t pos, int8_t const *priv);
uint32_t isequal(uint32_t a, uint32_t b);
void cmov(int8_t *r, const int8_t *a, uint32_t b);


#endif
