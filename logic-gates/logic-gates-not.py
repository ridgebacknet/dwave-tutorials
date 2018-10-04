"""
Copyright (C) 2018 Ridgeback Network Defense, Inc.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

from dwave.system.samplers import DWaveSampler
from neal import SimulatedAnnealingSampler

useQpu = False  # change this to use a live QPU

"""
logic-gates-not.py
------------------
  Tutorial for NOT logic gate.
  This is a fairly low-level tutorial.
  To use a live QPU, set useQpu to True.

This code returns solutions where:

    q0 = NOT(q4)

:q0: qubit 0 (value of 0 or 1)
:q4: qubit 4 (value of 0 or 1)

The lowest energies are the correct solutions. For this example, an
energy of -1 shows qubit combinations that solve the problem, and
an energy of greater than -1 shows qubit combinations that do not match
our problem. There is nothing special about -1; for quantum annealing,
lower energies are always better or more appropriate answers.

FAQ
---

Why did you choose qubits 0 and 4?
  Because, on the current D-Wave, qubits 0 and 4 have a coupling between
  them. Qubits 0 and 1 do not have a coupling between them. For the
  first cell on the QPU, here are the qubit couplings within the cell:
  ((0,4),(0,5),(0,6),(0,7),
   (1,4),(1,5),(1,6),(1,7),
   (2,4),(2,5),(2,6),(2,7),
   (3,4),(3,5),(3,6),(3,7))

References
----------

- https://docs.ocean.dwavesys.com/en/latest/examples/not.html

"""

print('')
print('Logic gate: NOT')
print('===============')
print('Given qubits q0 and q4, list possible solutions where:')
print('  q0 = NOT(q4)')
print('')

# At the top of this file, set useQpu to True to use a live QPU.
if (useQpu):
    sampler = DWaveSampler()
else:
    sampler = SimulatedAnnealingSampler()

# The Q variable is called the quadratic. It is a list of qubit biases
# and couplings. This configuration for NOT is equivalent to the
# equation:
#
#   energy = ( (q0 * -1) + (q0 * q4 * 0) + (q4 * q0 * 2) + (q4 * -1) )
#
# In plain language, we want energy to be the lowest possible value
# only when q0 and q4 are different.
Q = {(0, 0): -1, (0, 4): 0, (4, 0): 2, (4, 4): -1}

# A sampler returns one or more possible solutions. We are looking for
# solutions that have the lowest possible energy value. The num_reads
# argument means we want to try and solve this 20 times.
# Keep in mind:
#   - A QPU will do this in 20 atomic operations.
#   - A simulated annealer will run a probabilistic simulation 20 times.
# See: https://docs.ocean.dwavesys.com/projects/dimod/en/latest/reference/generated/dimod.Sampler.sample_qubo.html
response = sampler.sample_qubo(Q, num_reads=20)

# The data() function will return the results.
# See: https://docs.ocean.dwavesys.com/projects/dimod/en/latest/reference/generated/dimod.Response.data.html
# NOTE: As of 2018-09-30, the DWaveSampler() will aggregate the results,
# but the SimulatedAnnealingSampler will not.
print('List of possible solutions')
print('--------------------------')
for sample, energy, num_occurrences in response.data():
    print(sample, "Energy: ", energy, "Occurrences: ", num_occurrences)

"""
Sample output for DWaveSampler():

$ python3 logic-gates-not.py

Logic gate: NOT
===============
Given qubits q0 and q4, list possible solutions where:
  q0 = NOT(q4)

List of possible solutions
--------------------------
{0: 0, 4: 1} Energy:  -1.0 Occurrences:  15
{0: 1, 4: 0} Energy:  -1.0 Occurrences:  5
"""

"""
Sample output for SimulatedAnnealingSampler():

$ python3 logic-gates-not.py

Logic gate: NOT
===============
Given qubits q0 and q4, list possible solutions where:
  q0 = NOT(q4)

List of possible solutions
--------------------------
{0: 0, 4: 1} Energy:  -1.0 Occurrences:  1
{0: 1, 4: 0} Energy:  -1.0 Occurrences:  1
{0: 0, 4: 1} Energy:  -1.0 Occurrences:  1
{0: 0, 4: 1} Energy:  -1.0 Occurrences:  1
{0: 1, 4: 0} Energy:  -1.0 Occurrences:  1
{0: 0, 4: 1} Energy:  -1.0 Occurrences:  1
{0: 1, 4: 0} Energy:  -1.0 Occurrences:  1
{0: 1, 4: 0} Energy:  -1.0 Occurrences:  1
{0: 0, 4: 1} Energy:  -1.0 Occurrences:  1
{0: 0, 4: 1} Energy:  -1.0 Occurrences:  1
{0: 1, 4: 0} Energy:  -1.0 Occurrences:  1
{0: 1, 4: 0} Energy:  -1.0 Occurrences:  1
{0: 0, 4: 1} Energy:  -1.0 Occurrences:  1
{0: 1, 4: 1} Energy:  0.0 Occurrences:  1
{0: 1, 4: 1} Energy:  0.0 Occurrences:  1
{0: 0, 4: 0} Energy:  0.0 Occurrences:  1
{0: 0, 4: 0} Energy:  0.0 Occurrences:  1
{0: 0, 4: 0} Energy:  0.0 Occurrences:  1
{0: 0, 4: 0} Energy:  0.0 Occurrences:  1
{0: 0, 4: 0} Energy:  0.0 Occurrences:  1
"""
