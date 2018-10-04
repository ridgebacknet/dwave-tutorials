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
from dwave.system.composites import EmbeddingComposite

useQpu = False  # change this to use a live QPU

"""
logic-gates-and.py
------------------
  Tutorial for AND logic gate.
  This is a fairly low-level tutorial.
  To use a live QPU, set useQpu to True.

This code returns solutions where:

    z = AND(x1, x2)

:x1: virtual qubit (value of 0 or 1)
:x2: virtual qubit (value of 0 or 1)
:z: virtual qubit (value of 0 or 1)

The lowest energies are the correct solutions. For this example, an
energy of 0 shows qubit combinations that solve the problem, and
an energy of greater than 0 shows qubit combinations that do not match
our problem. There is nothing special about 0; for quantum annealing,
lower energies are always better or more appropriate answers.

This tutorial is based on the D-Wave Ocean Tools documentation for a
boolean AND gate.

FAQ
---

What are virtual qubits?
  On the current D-Wave topology, called Chimera, there are no
  triangles. However, we need a triangle configuration to make an AND
  gate. There is a tool called VirtualGraphComposite that allows us
  to work with virtual qubits; VirtualGraphComposite will map our
  virtual qubits to physical qubits.

Do virtual qubits impact performance?
  Yes, virtual qubits can increase the space complexity of the problem.
  That means the number of physical qubits may be greater than the
  number of virtual qubits, and we only have a limited number of
  physical qubits. There are techniques to solve problems that need
  more physical qubits than you have, but that is a subject for a
  different tutorial. Also, D-Wave is working on a new QPU topology
  called Pegasus, which will dramtically reduce the number of extra
  physical qubits you need when using virtual qubits.

Why is the last entry for the simulated annealer incorrect?
  The last entry from the simulated annealer shows:
    {'x1': 1, 'x2': 1, 'z': 0} Energy:  1.0 Occurrences:  1
  This is like saying 0 = AND(1,1), which is obviously wrong.
  It is important to note that the energy is 1.0, which is higher than
  all the rest. The point of quantum annealing is to find solutions with
  the lowest energy values. For this one case, the probabilistic
  simulator randomly found a solution that was incorrect, but it did
  correctly tell us that it was incorrect. Keep this in mind when you
  tackle very hard problems. That energy value will always let you know
  how good a possible solution is. In case you are wondering, the last
  time I checked, the simulated annealer was using the xorshift128+
  algorithm to generate its pseudo-random numbers.

References
----------

- https://docs.ocean.dwavesys.com/en/latest/examples/and.html

"""

print('')
print('Logic gate: AND')
print('===============')
print('Given virtual qubits x1, x2, and z, list possible solutions where:')
print('  z = AND(x1, x2)')
print('')

# At the top of this file, set useQpu to True to use a live QPU.
#
# For this tutorial we need a triangular configution, but the physical
# topology of the QPU does not have triangles. There is a technique
# called "embedding" that allows us to map our virtual problem onto a
# physical platform. The concept of embedding is described more
# thoroughly in the embedding tutorials.
if (useQpu):
    sampler = DWaveSampler()  # live QPU
    sampler_embedded = EmbeddingComposite(sampler)  # we will need to embed
else:
    sampler = SimulatedAnnealingSampler()  # simulated quantum annealer
    sampler_embedded = sampler  # we do not need to embed for a simulation

# The Q variable is called the quadratic. It is a list of qubit biases
# and couplings. This configuration for AND is equivalent to the
# equation:
#
#   energy = ( (x1 * x2 * 1) + (x1 * z * -2) + (x2 * z * -2) + (z * 3) )
#
# In plain language, we want energy to be the lowest possible value
# only when z is the boolean AND of x1 and x2, or when z = x1 * x2.
Q = {('x1', 'x2'): 1, ('x1', 'z'): -2, ('x2', 'z'): -2, ('z', 'z'): 3}

# A sampler returns one or more possible solutions. We are looking for
# solutions that have the lowest possible energy value. The num_reads
# argument means we want to try and solve this 40 times.
# Keep in mind:
#   - A QPU will do this in 40 atomic operations.
#   - A simulated annealer will run a probabilistic simulation 40 times.
# See: https://docs.ocean.dwavesys.com/projects/dimod/en/latest/reference/generated/dimod.Sampler.sample_qubo.html
response = sampler_embedded.sample_qubo(Q, num_reads=40)

# The data() function will return the results.
# See: https://docs.ocean.dwavesys.com/projects/dimod/en/latest/reference/generated/dimod.Response.data.html
# NOTE: As of 2018-09-30, the DWaveSampler() will aggregate the results,
# but the SimulatedAnnealingSampler will not.
print('List of possible solutions')
print('--------------------------')
for sample, energy, num_occurrences in response.data():
    print(sample, "Energy: ", energy, "Occurrences: ", num_occurrences)

"""
Sample output for EmbeddingComposite(DWaveSampler()):

$ python3 logic-gates-and.py

Logic gate: AND
===============
Given virtual qubits x1, x2, and z, list possible solutions where:
  z = AND(x1, x2)

List of possible solutions
--------------------------
{'z': 0, 'x1': 1, 'x2': 0} Energy:  0.0 Occurrences:  7
{'z': 1, 'x1': 1, 'x2': 1} Energy:  0.0 Occurrences:  9
{'z': 0, 'x1': 0, 'x2': 0} Energy:  0.0 Occurrences:  12
{'z': 0, 'x1': 0, 'x2': 1} Energy:  0.0 Occurrences:  12
"""

"""
Sample output for SimulatedAnnealingSampler():

$ python3 logic-gates-and.py

Logic gate: AND
===============
Given virtual qubits x1, x2, and z, list possible solutions where:
  z = AND(x1, x2)

List of possible solutions
--------------------------
{'x1': 0, 'x2': 0, 'z': 0} Energy:  0.0 Occurrences:  1
{'x1': 1, 'x2': 0, 'z': 0} Energy:  0.0 Occurrences:  1
{'x1': 1, 'x2': 1, 'z': 1} Energy:  0.0 Occurrences:  1
{'x1': 1, 'x2': 1, 'z': 1} Energy:  0.0 Occurrences:  1
{'x1': 0, 'x2': 0, 'z': 0} Energy:  0.0 Occurrences:  1
{'x1': 1, 'x2': 1, 'z': 1} Energy:  0.0 Occurrences:  1
{'x1': 1, 'x2': 0, 'z': 0} Energy:  0.0 Occurrences:  1
{'x1': 0, 'x2': 1, 'z': 0} Energy:  0.0 Occurrences:  1
{'x1': 1, 'x2': 1, 'z': 1} Energy:  0.0 Occurrences:  1
{'x1': 1, 'x2': 1, 'z': 1} Energy:  0.0 Occurrences:  1
{'x1': 1, 'x2': 0, 'z': 0} Energy:  0.0 Occurrences:  1
{'x1': 0, 'x2': 1, 'z': 0} Energy:  0.0 Occurrences:  1
{'x1': 1, 'x2': 1, 'z': 1} Energy:  0.0 Occurrences:  1
{'x1': 1, 'x2': 1, 'z': 1} Energy:  0.0 Occurrences:  1
{'x1': 1, 'x2': 0, 'z': 0} Energy:  0.0 Occurrences:  1
{'x1': 1, 'x2': 0, 'z': 0} Energy:  0.0 Occurrences:  1
{'x1': 1, 'x2': 1, 'z': 1} Energy:  0.0 Occurrences:  1
{'x1': 1, 'x2': 1, 'z': 1} Energy:  0.0 Occurrences:  1
{'x1': 0, 'x2': 0, 'z': 0} Energy:  0.0 Occurrences:  1
{'x1': 1, 'x2': 1, 'z': 1} Energy:  0.0 Occurrences:  1
{'x1': 1, 'x2': 1, 'z': 1} Energy:  0.0 Occurrences:  1
{'x1': 0, 'x2': 0, 'z': 0} Energy:  0.0 Occurrences:  1
{'x1': 1, 'x2': 1, 'z': 1} Energy:  0.0 Occurrences:  1
{'x1': 1, 'x2': 1, 'z': 1} Energy:  0.0 Occurrences:  1
{'x1': 0, 'x2': 0, 'z': 0} Energy:  0.0 Occurrences:  1
{'x1': 0, 'x2': 0, 'z': 0} Energy:  0.0 Occurrences:  1
{'x1': 1, 'x2': 0, 'z': 0} Energy:  0.0 Occurrences:  1
{'x1': 1, 'x2': 1, 'z': 1} Energy:  0.0 Occurrences:  1
{'x1': 0, 'x2': 1, 'z': 0} Energy:  0.0 Occurrences:  1
{'x1': 1, 'x2': 0, 'z': 0} Energy:  0.0 Occurrences:  1
{'x1': 1, 'x2': 0, 'z': 0} Energy:  0.0 Occurrences:  1
{'x1': 0, 'x2': 1, 'z': 0} Energy:  0.0 Occurrences:  1
{'x1': 0, 'x2': 1, 'z': 0} Energy:  0.0 Occurrences:  1
{'x1': 0, 'x2': 1, 'z': 0} Energy:  0.0 Occurrences:  1
{'x1': 0, 'x2': 0, 'z': 0} Energy:  0.0 Occurrences:  1
{'x1': 0, 'x2': 1, 'z': 0} Energy:  0.0 Occurrences:  1
{'x1': 0, 'x2': 0, 'z': 0} Energy:  0.0 Occurrences:  1
{'x1': 0, 'x2': 0, 'z': 0} Energy:  0.0 Occurrences:  1
{'x1': 0, 'x2': 1, 'z': 0} Energy:  0.0 Occurrences:  1
{'x1': 1, 'x2': 1, 'z': 0} Energy:  1.0 Occurrences:  1
"""
