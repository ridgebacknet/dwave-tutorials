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
import dwavebinarycsp
import dwavebinarycsp.factories.constraint.gates as gates
import operator

useQpu = False  # change this to use a live QPU

"""
logic-gates-full-adder.py
-------------------------
  Tutorial for a full-adder cicuit.
  To use a live QPU, set useQpu to True.

This code returns solutions where:

    (s, cOut) = a + b + cIn

:a: input; virtual qubit (value of 0 or 1)
:b: input; virtual qubit (value of 0 or 1)
:cIn: the carry bit input; virtual qubit (value of 0 or 1)
:s: the sum of a + b + cIn; virtual qubit (value of 0 or 1)
:cOut: the carry bit from a + b + cIn; virtual qubit (value of 0 or 1)

The lowest energies are the correct solutions.
For this example, the answers are very probabilistic. Therefore, for
each possible solution we check our constraints to see if the solution
is valid. The problem we are solving is NP-complete. This implies
finding solutions is hard, but checking a solution is easy.

This tutorial is based on the D-Wave Ocean Tools documentation for a
multiple-gate cicuit.

Requirements
------------

This tutorial uses the Python package PySMT to create a graph that can
be embedded on the D-Wave. In case you have trouble with PySMT
complaining about not finding a solver, try these commands:

```
pysmt-install --help
pysmt-install --check
pysmt-install --env
```

FAQ
---

How hard is the problem we are solving?
  The type of problem we are solving is NP-complete. In plain language,
  it is very hard to find a solution for an NP-complete problem, but
  it is relatively straightforward to check a possible solution for
  correctness. Since the problem we are solving is very small, it is
  actually inefficient to use a quantum computer. However, it is a good
  problem to learn with.

Why do I have to check the solutions?
  To put it bluntly, we are using a sledgehammer to put in a screw.
  Although we are only interested in binary variables, quantum annealing
  is using real probabilities behind the scenes. Not only do we need to
  fit our problem to the underlying topology of the underlying hardware,
  but we also have to tune the qubit biases and couplings to match that
  embedding. Getting a perfect fit automatically is a very hard problem
  by itself. So, we make a tradeoff -- we use
  dwavebinarycsp.ConstraintSatisfactionProblem as a very easy-to-use
  tool, but then our fit to the hardware is kind of up in the air.
  At the end of the day, the dwavebinarycsp package is a great
  prototyping tool, but not-so-great if we want optimal solutions.

Why does the simulated annealer generate far more correct solutions?
  The simulated annealer does not need to fit the topology of the
  problem to the topology of a physical QPU. For a simulated annealer
  we run the simulation as if every qubit is connected to every other
  qubit. A physical QPU is limited by topology, and whether the
  automated tools fit the problem well or not is pretty much left to
  chance. That does not mean that a good fit is not possible, but it
  does mean that using prototyping tools usually will not get you the
  best performance. The best analogy is optimizing compilers. Making a
  basic compiler that goes from a high-level language to machine code
  is not that hard. However, it took a lot of work before people figured
  out the best ways to have compilers generate optimal code.

What is this topology stuff?
  When I say topology, I am referring to connectivity. On the D-Wave
  Chimera chips, each qubit is connected to either six or five other
  qubits. That is limitting for many problems. The next version of the
  D-Wave chip is called Pegasus. Pegasus is supposed to have fifteen
  connections per qubit, which would be an incredible boost in
  performance, and much easier to fit problems to.

References
----------

- https://docs.ocean.dwavesys.com/en/latest/examples/multi_gate.html
- https://en.wikipedia.org/wiki/Adder_(electronics)
- https://docs.ocean.dwavesys.com/projects/binarycsp/en/latest/reference/index.html

"""

print('')
print('Logic gate: full-adder')
print('======================')
print('Given virtual qubits a, b, cIn, s, cOut, list possible solutions where:')
print('  s = a + b + cIn, with carry bit in cOut')
print('  This is a full-adder cicuit.')
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

# The ConstraintSatisfactionProblem class is wonderful for prototyping
# code on the D-Wave.
# https://docs.ocean.dwavesys.com/projects/binarycsp/en/latest/reference/csp.html
csp = dwavebinarycsp.ConstraintSatisfactionProblem(dwavebinarycsp.BINARY)

"""
Now we tie together logic gates and operators in the form of
constraints. Listing constraints is an easy way to get a problem onto
the D-Wave, but it is not necessarily an optimal way to do it.

Gates that are allowed include:
  and_gate 
  or_gate
  xor_gate
  halfadder_gate
Logical operators that are allowed include:
  not_
  truth
  is_
  is_not
Comparison operators that are allowed include:
  lt
  le
  eq
  ne
  ge
  gt

For the full-adder we will use:
  inputs (a, b, Cin)
  outputs (s, cOut)

For the intermediate variables we will use:
  (xor1, xor2, and1, and2, or1)
However, s and xor2 are the same, and cOut and or1 are the same.

See this image for a graphical view of this circuit:
https://upload.wikimedia.org/wikipedia/commons/5/57/Fulladder.gif
"""

csp.add_constraint(gates.xor_gate(['a',    'b',   'xor1' ]))  # xor(a,b) = xor1

csp.add_constraint(gates.xor_gate(['xor1', 'cIn', 's'    ]))  # xor(xor1,cIn) = s
csp.add_constraint(gates.and_gate(['xor1', 'cIn', 'and1' ]))  # and(xor1,cIn) = and1
csp.add_constraint(gates.and_gate(['a',    'b',   'and2' ]))  # and(a,b) = and2

csp.add_constraint(gates.or_gate( ['and1', 'and2', 'cOut']))  # or(and1,and2) = cOut

# This is an example of an assert I used to ensure my constraints above
# faithfully reproduced the full-adder I want to implement.
# https://docs.ocean.dwavesys.com/projects/binarycsp/en/latest/reference/generated/dwavebinarycsp.ConstraintSatisfactionProblem.check.html
assert csp.check({'a': 1, 'and1': 0, 'and2': 1, 'b': 1, 'cIn': 0, 'cOut': 1, 's': 0, 'xor1': 0})

# By adding constraints, we have declared what is and is not acceptible
# in solutions. That list of constraints needs to be mapped to a
# "binary quadratic model," which is that list of biases and couplings
# that were used in the NOT and AND tutorials. The stitch() function
# basically generates all of our virtual qubits.

print('Begin stitching...')
# I boost the min_classical_gap from 2.0 (default) to 3.0 to get a
# little better accuracy. Be careful, though, numbers larger that 4.0
# can take a long time to compute.
# https://docs.ocean.dwavesys.com/projects/binarycsp/en/latest/reference/generated/dwavebinarycsp.stitch.html
bqm = dwavebinarycsp.stitch(csp, min_classical_gap=3.0)
print('Done stitching.')

if (useQpu):
    maxReads = 5000 # use many samples for a QPU
else:
    maxReads = 30   # use few samples for a simulated annealer

# Here we ask our sampler for possible solutions. The argument
# num_reads sets how many possible solutions we want back in one batch.
# If we are using a live QPU, the embedded sampler from above will
# automatically map our virtual qubits onto the physical qubits.
# The mapping process is called embedding. Keep in mind that automatic
# embedding is usually worse than embedding by hand because there is
# still a lot to be learned about how to make the best embeddings for
# different kinds of problems.
    
print('Begin sampling...')
response = sampler_embedded.sample(bqm, num_reads = maxReads)
print('Done sampling.')

# Now that we have a bunch of possible solutions, we need to sort
# through them and check to see which ones are valid. We can get
# invalid solutions because the automatic embedding process is
# far from perfect. Again, this not necessarily a problem with the
# hardware, but more a reflection of how far we need to go to improve
# the software tools.
#
# Until we have better embedding tools, we expect more valid solutions
# from the simulated annealer. If we want all or many of the valid
# solutions, then we need to look into how to make the best embedding
# possible. However, sometimes we only need a single valid solution.
# If we only need one valid solution, then a mediocre embedding might
# be fine.

valid, invalid = 0, 0
for datum in response.data():
    sample, energy, num = datum
    if (csp.check(sample)):
        print(datum)  # print all valid solutions we find
        valid = valid+num
    else:
        invalid = invalid+num
print(valid, ' valid solutions, ', invalid, ' invalid solutions')


"""
Listed below is sample output using the DWaveSampler. To get valid
solutions, you might have to run it more than once. This is because
the combined stitch() and embedding you get might be unlucky.

$ python3 logic-gates-full-adder.py

Logic gate: full-adder
======================
Given virtual qubits a, b, cIn, s, cOut, list possible solutions where:
  s = a + b + cIn, with carry bit in cOut
  This is a full-adder cicuit.

Begin stitching...
Done stitching.
Begin sampling...
Done sampling.
Sample(sample={'a': 1, 'aux0': 1, 'aux1': 0, 'aux2': 0, 'b': 0, 'xor1': 1, 'aux3': 1, 'aux4': 0, 'aux5': 0, 'cIn': 1, 's': 0, 'and1': 1, 'aux6': 0, 'and2': 0, 'aux7': 1, 'aux8': 0, 'cOut': 1}, energy=-24.987500000000004, num_occurrences=2)
Sample(sample={'a': 1, 'aux0': 1, 'aux1': 0, 'aux2': 0, 'b': 0, 'xor1': 1, 'aux3': 1, 'aux4': 1, 'aux5': 0, 'cIn': 1, 's': 0, 'and1': 1, 'aux6': 0, 'and2': 0, 'aux7': 1, 'aux8': 0, 'cOut': 1}, energy=-20.987500000000004, num_occurrences=1)
Sample(sample={'a': 1, 'aux0': 1, 'aux1': 1, 'aux2': 0, 'b': 0, 'xor1': 1, 'aux3': 1, 'aux4': 0, 'aux5': 0, 'cIn': 1, 's': 0, 'and1': 1, 'aux6': 0, 'and2': 0, 'aux7': 1, 'aux8': 0, 'cOut': 1}, energy=-20.987500000000004, num_occurrences=36)
Sample(sample={'a': 1, 'aux0': 1, 'aux1': 1, 'aux2': 0, 'b': 0, 'xor1': 1, 'aux3': 1, 'aux4': 0, 'aux5': 0, 'cIn': 1, 's': 0, 'and1': 1, 'aux6': 0, 'and2': 0, 'aux7': 1, 'aux8': 0, 'cOut': 1}, energy=-20.987500000000004, num_occurrences=1)
Sample(sample={'a': 1, 'aux0': 1, 'aux1': 1, 'aux2': 0, 'b': 0, 'xor1': 1, 'aux3': 1, 'aux4': 1, 'aux5': 0, 'cIn': 1, 's': 0, 'and1': 1, 'aux6': 0, 'and2': 0, 'aux7': 1, 'aux8': 0, 'cOut': 1}, energy=-16.987500000000004, num_occurrences=1)
Sample(sample={'a': 1, 'aux0': 1, 'aux1': 1, 'aux2': 0, 'b': 0, 'xor1': 1, 'aux3': 1, 'aux4': 1, 'aux5': 0, 'cIn': 1, 's': 0, 'and1': 1, 'aux6': 0, 'and2': 0, 'aux7': 1, 'aux8': 0, 'cOut': 1}, energy=-16.987500000000004, num_occurrences=59)
Sample(sample={'a': 1, 'aux0': 1, 'aux1': 1, 'aux2': 0, 'b': 0, 'xor1': 1, 'aux3': 1, 'aux4': 1, 'aux5': 0, 'cIn': 1, 's': 0, 'and1': 1, 'aux6': 0, 'and2': 0, 'aux7': 1, 'aux8': 0, 'cOut': 1}, energy=-16.987500000000004, num_occurrences=51)
Sample(sample={'a': 1, 'aux0': 1, 'aux1': 1, 'aux2': 0, 'b': 0, 'xor1': 1, 'aux3': 1, 'aux4': 1, 'aux5': 0, 'cIn': 1, 's': 0, 'and1': 1, 'aux6': 0, 'and2': 0, 'aux7': 1, 'aux8': 0, 'cOut': 1}, energy=-16.987500000000004, num_occurrences=1)
152  valid solutions,  4848  invalid solutions
"""

"""
And here is sample output from the simulated annealer. It works better
because the methods we are using for embedding are a gamble, while the
simulated annealer does not need to worry about embedding.

$ python3 logic-gates-full-adder.py

Logic gate: full-adder
======================
Given virtual qubits a, b, cIn, s, cOut, list possible solutions where:
  s = a + b + cIn, with carry bit in cOut
  This is a full-adder cicuit.

Begin stitching...
Done stitching.
Begin sampling...
Done sampling.
Sample(sample={'a': 1, 'and1': 0, 'and2': 0, 'aux0': 1, 'aux1': 0, 'aux2': 0, 'aux3': 1, 'aux4': 0, 'aux5': 1, 'aux6': 1, 'aux7': 1, 'aux8': 1, 'b': 0, 'cIn': 0, 'cOut': 0, 's': 1, 'xor1': 1}, energy=-24.987500000000008, num_occurrences=1)
Sample(sample={'a': 0, 'and1': 0, 'and2': 0, 'aux0': 1, 'aux1': 1, 'aux2': 1, 'aux3': 0, 'aux4': 0, 'aux5': 1, 'aux6': 1, 'aux7': 1, 'aux8': 1, 'b': 0, 'cIn': 1, 'cOut': 0, 's': 1, 'xor1': 0}, energy=-24.987500000000008, num_occurrences=1)
Sample(sample={'a': 0, 'and1': 0, 'and2': 0, 'aux0': 1, 'aux1': 1, 'aux2': 1, 'aux3': 1, 'aux4': 1, 'aux5': 1, 'aux6': 1, 'aux7': 1, 'aux8': 1, 'b': 0, 'cIn': 0, 'cOut': 0, 's': 0, 'xor1': 0}, energy=-24.987500000000008, num_occurrences=1)
Sample(sample={'a': 1, 'and1': 0, 'and2': 0, 'aux0': 1, 'aux1': 0, 'aux2': 0, 'aux3': 1, 'aux4': 0, 'aux5': 1, 'aux6': 1, 'aux7': 1, 'aux8': 1, 'b': 0, 'cIn': 0, 'cOut': 0, 's': 1, 'xor1': 1}, energy=-24.987500000000008, num_occurrences=1)
Sample(sample={'a': 1, 'and1': 0, 'and2': 0, 'aux0': 1, 'aux1': 0, 'aux2': 0, 'aux3': 1, 'aux4': 0, 'aux5': 1, 'aux6': 1, 'aux7': 1, 'aux8': 1, 'b': 0, 'cIn': 0, 'cOut': 0, 's': 1, 'xor1': 1}, energy=-24.987500000000008, num_occurrences=1)
Sample(sample={'a': 0, 'and1': 0, 'and2': 0, 'aux0': 1, 'aux1': 1, 'aux2': 1, 'aux3': 1, 'aux4': 1, 'aux5': 1, 'aux6': 1, 'aux7': 1, 'aux8': 1, 'b': 0, 'cIn': 0, 'cOut': 0, 's': 0, 'xor1': 0}, energy=-24.987500000000008, num_occurrences=1)
Sample(sample={'a': 0, 'and1': 0, 'and2': 0, 'aux0': 1, 'aux1': 1, 'aux2': 1, 'aux3': 1, 'aux4': 1, 'aux5': 1, 'aux6': 1, 'aux7': 1, 'aux8': 1, 'b': 0, 'cIn': 0, 'cOut': 0, 's': 0, 'xor1': 0}, energy=-24.987500000000008, num_occurrences=1)
Sample(sample={'a': 0, 'and1': 0, 'and2': 0, 'aux0': 1, 'aux1': 1, 'aux2': 1, 'aux3': 0, 'aux4': 0, 'aux5': 1, 'aux6': 1, 'aux7': 1, 'aux8': 1, 'b': 0, 'cIn': 1, 'cOut': 0, 's': 1, 'xor1': 0}, energy=-24.987500000000008, num_occurrences=1)
Sample(sample={'a': 1, 'and1': 0, 'and2': 0, 'aux0': 1, 'aux1': 0, 'aux2': 0, 'aux3': 1, 'aux4': 0, 'aux5': 1, 'aux6': 1, 'aux7': 1, 'aux8': 1, 'b': 0, 'cIn': 0, 'cOut': 0, 's': 1, 'xor1': 1}, energy=-24.987500000000008, num_occurrences=1)
Sample(sample={'a': 0, 'and1': 1, 'and2': 0, 'aux0': 0, 'aux1': 0, 'aux2': 1, 'aux3': 1, 'aux4': 0, 'aux5': 0, 'aux6': 0, 'aux7': 1, 'aux8': 0, 'b': 1, 'cIn': 1, 'cOut': 1, 's': 0, 'xor1': 1}, energy=-24.987500000000008, num_occurrences=1)
Sample(sample={'a': 0, 'and1': 1, 'and2': 0, 'aux0': 0, 'aux1': 0, 'aux2': 1, 'aux3': 1, 'aux4': 0, 'aux5': 0, 'aux6': 0, 'aux7': 1, 'aux8': 0, 'b': 1, 'cIn': 1, 'cOut': 1, 's': 0, 'xor1': 1}, energy=-24.987500000000008, num_occurrences=1)
Sample(sample={'a': 1, 'and1': 0, 'and2': 1, 'aux0': 1, 'aux1': 0, 'aux2': 1, 'aux3': 0, 'aux4': 0, 'aux5': 1, 'aux6': 1, 'aux7': 0, 'aux8': 0, 'b': 1, 'cIn': 1, 'cOut': 1, 's': 1, 'xor1': 0}, energy=-24.987500000000008, num_occurrences=1)
Sample(sample={'a': 0, 'and1': 0, 'and2': 0, 'aux0': 1, 'aux1': 1, 'aux2': 1, 'aux3': 0, 'aux4': 0, 'aux5': 1, 'aux6': 1, 'aux7': 1, 'aux8': 1, 'b': 0, 'cIn': 1, 'cOut': 0, 's': 1, 'xor1': 0}, energy=-24.987500000000008, num_occurrences=1)
Sample(sample={'a': 1, 'and1': 1, 'and2': 0, 'aux0': 1, 'aux1': 0, 'aux2': 0, 'aux3': 1, 'aux4': 0, 'aux5': 0, 'aux6': 0, 'aux7': 1, 'aux8': 0, 'b': 0, 'cIn': 1, 'cOut': 1, 's': 0, 'xor1': 1}, energy=-24.987500000000008, num_occurrences=1)
Sample(sample={'a': 1, 'and1': 0, 'and2': 1, 'aux0': 1, 'aux1': 0, 'aux2': 1, 'aux3': 0, 'aux4': 0, 'aux5': 1, 'aux6': 1, 'aux7': 0, 'aux8': 0, 'b': 1, 'cIn': 1, 'cOut': 1, 's': 1, 'xor1': 0}, energy=-24.987500000000008, num_occurrences=1)
Sample(sample={'a': 1, 'and1': 0, 'and2': 1, 'aux0': 1, 'aux1': 0, 'aux2': 1, 'aux3': 0, 'aux4': 0, 'aux5': 1, 'aux6': 1, 'aux7': 0, 'aux8': 0, 'b': 1, 'cIn': 1, 'cOut': 1, 's': 1, 'xor1': 0}, energy=-24.987500000000008, num_occurrences=1)
Sample(sample={'a': 0, 'and1': 1, 'and2': 0, 'aux0': 0, 'aux1': 0, 'aux2': 1, 'aux3': 1, 'aux4': 0, 'aux5': 0, 'aux6': 0, 'aux7': 1, 'aux8': 0, 'b': 1, 'cIn': 1, 'cOut': 1, 's': 0, 'xor1': 1}, energy=-24.987500000000008, num_occurrences=1)
Sample(sample={'a': 0, 'and1': 1, 'and2': 0, 'aux0': 0, 'aux1': 0, 'aux2': 1, 'aux3': 1, 'aux4': 0, 'aux5': 0, 'aux6': 0, 'aux7': 1, 'aux8': 0, 'b': 1, 'cIn': 1, 'cOut': 1, 's': 0, 'xor1': 1}, energy=-24.987500000000008, num_occurrences=1)
Sample(sample={'a': 1, 'and1': 0, 'and2': 1, 'aux0': 1, 'aux1': 0, 'aux2': 1, 'aux3': 0, 'aux4': 0, 'aux5': 1, 'aux6': 1, 'aux7': 0, 'aux8': 0, 'b': 1, 'cIn': 1, 'cOut': 1, 's': 1, 'xor1': 0}, energy=-24.987500000000008, num_occurrences=1)
Sample(sample={'a': 1, 'and1': 0, 'and2': 0, 'aux0': 1, 'aux1': 0, 'aux2': 0, 'aux3': 1, 'aux4': 0, 'aux5': 1, 'aux6': 1, 'aux7': 1, 'aux8': 1, 'b': 0, 'cIn': 0, 'cOut': 0, 's': 1, 'xor1': 1}, energy=-24.987500000000008, num_occurrences=1)
Sample(sample={'a': 0, 'and1': 0, 'and2': 0, 'aux0': 0, 'aux1': 0, 'aux2': 1, 'aux3': 1, 'aux4': 0, 'aux5': 1, 'aux6': 1, 'aux7': 1, 'aux8': 1, 'b': 1, 'cIn': 0, 'cOut': 0, 's': 1, 'xor1': 1}, energy=-24.987500000000004, num_occurrences=1)
Sample(sample={'a': 0, 'and1': 0, 'and2': 0, 'aux0': 0, 'aux1': 0, 'aux2': 1, 'aux3': 1, 'aux4': 0, 'aux5': 1, 'aux6': 1, 'aux7': 1, 'aux8': 1, 'b': 1, 'cIn': 0, 'cOut': 0, 's': 1, 'xor1': 1}, energy=-24.987500000000004, num_occurrences=1)
Sample(sample={'a': 1, 'and1': 0, 'and2': 1, 'aux0': 1, 'aux1': 0, 'aux2': 1, 'aux3': 1, 'aux4': 1, 'aux5': 1, 'aux6': 1, 'aux7': 0, 'aux8': 0, 'b': 1, 'cIn': 0, 'cOut': 1, 's': 0, 'xor1': 0}, energy=-24.987500000000004, num_occurrences=1)
Sample(sample={'a': 1, 'and1': 0, 'and2': 1, 'aux0': 1, 'aux1': 0, 'aux2': 1, 'aux3': 1, 'aux4': 1, 'aux5': 1, 'aux6': 1, 'aux7': 0, 'aux8': 0, 'b': 1, 'cIn': 0, 'cOut': 1, 's': 0, 'xor1': 0}, energy=-24.987500000000004, num_occurrences=1)
Sample(sample={'a': 0, 'and1': 0, 'and2': 0, 'aux0': 0, 'aux1': 0, 'aux2': 1, 'aux3': 1, 'aux4': 0, 'aux5': 1, 'aux6': 1, 'aux7': 1, 'aux8': 1, 'b': 1, 'cIn': 0, 'cOut': 0, 's': 1, 'xor1': 1}, energy=-24.987500000000004, num_occurrences=1)
Sample(sample={'a': 0, 'and1': 0, 'and2': 0, 'aux0': 0, 'aux1': 0, 'aux2': 1, 'aux3': 1, 'aux4': 0, 'aux5': 1, 'aux6': 1, 'aux7': 1, 'aux8': 1, 'b': 1, 'cIn': 0, 'cOut': 0, 's': 1, 'xor1': 1}, energy=-24.987500000000004, num_occurrences=1)
Sample(sample={'a': 1, 'and1': 0, 'and2': 1, 'aux0': 1, 'aux1': 0, 'aux2': 1, 'aux3': 1, 'aux4': 1, 'aux5': 1, 'aux6': 1, 'aux7': 0, 'aux8': 0, 'b': 1, 'cIn': 0, 'cOut': 1, 's': 0, 'xor1': 0}, energy=-24.987500000000004, num_occurrences=1)
Sample(sample={'a': 0, 'and1': 0, 'and2': 0, 'aux0': 0, 'aux1': 0, 'aux2': 1, 'aux3': 1, 'aux4': 0, 'aux5': 1, 'aux6': 1, 'aux7': 1, 'aux8': 1, 'b': 1, 'cIn': 0, 'cOut': 0, 's': 1, 'xor1': 1}, energy=-24.987500000000004, num_occurrences=1)
Sample(sample={'a': 1, 'and1': 0, 'and2': 1, 'aux0': 1, 'aux1': 0, 'aux2': 1, 'aux3': 1, 'aux4': 1, 'aux5': 1, 'aux6': 1, 'aux7': 0, 'aux8': 0, 'b': 1, 'cIn': 0, 'cOut': 1, 's': 0, 'xor1': 0}, energy=-24.987500000000004, num_occurrences=1)
Sample(sample={'a': 0, 'and1': 0, 'and2': 0, 'aux0': 0, 'aux1': 0, 'aux2': 1, 'aux3': 1, 'aux4': 0, 'aux5': 1, 'aux6': 1, 'aux7': 1, 'aux8': 1, 'b': 1, 'cIn': 0, 'cOut': 0, 's': 1, 'xor1': 1}, energy=-24.987500000000004, num_occurrences=1)
30  valid solutions,  0  invalid solutions
"""
