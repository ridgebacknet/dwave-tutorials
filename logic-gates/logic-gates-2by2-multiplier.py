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
logic-gates-2by2-multiplier.py
------------------------------
  Tutorial for factoring with a 2 by 2 multiplier cicuit.
  This tutorial also contains a technique for factoring numbers.
  To use a live QPU, set useQpu to True.

This code returns solutions where:

  (c3, c2, c1, c0) = (a1, a0) * (b1, b0), or
  C = A * B

:a0: input; virtual qubit (value of 0 or 1)
:a1: input; virtual qubit (value of 0 or 1)
:b0: input; virtual qubit (value of 0 or 1)
:b1: input; virtual qubit (value of 0 or 1)
:c0: input; virtual qubit (value of 0 or 1)
:c1: input; virtual qubit (value of 0 or 1)
:c2: input; virtual qubit (value of 0 or 1)
:c3: input; virtual qubit (value of 0 or 1)

A is a 2-bit number, where A = ((a1 * 2) + a0).
B is a 2-bit number, where B = ((b1 * 2) + b0).
C is a 4-bit number, where C = ((c3 * 8) + (c2 * 4) + (c1 * 2) + c0).

We are going to set the values of C, so when we look for solutions we
will actually get the factors of C.

The lowest energies are the correct solutions.
For this example, the answers are very probabilistic. Therefore, for
each possible solution we check our constraints to see if the solution
is valid. The approach we are using to factor is NP-complete. This
implies finding solutions is hard, but checking a solution is easy.
There are other ways to factor, and it is unlikely that the best
algorithms for factoring are NP-complete.

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
  The problem we are solving is circuit satisfiability, or CSAT.
  The approach we are using is NP-complete. In plain language,
  it is very hard to find a solution for an NP-complete problem, but
  it is relatively straightforward to check a possible solution for
  correctness. Since the problem we are solving is very small, it is
  actually inefficient to use a quantum computer. However, it is a good
  problem to learn with.

Can I use this problem to factor larger numbers?
  In theory, yes. There is some active research on this. The issue you
  will run into is that using random embeddings is not a very efficient
  strategy. It would be better to build an embedder that specializes in
  factoring problems.

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

- https://en.wikipedia.org/wiki/Binary_multiplier#/media/File:Binary_multi1.jpg
- https://en.wikipedia.org/wiki/Binary_multiplier
- https://en.wikipedia.org/wiki/Circuit_satisfiability_problem
- https://docs.ocean.dwavesys.com/en/latest/examples/multi_gate.html
- https://docs.ocean.dwavesys.com/projects/binarycsp/en/latest/reference/index.html
- https://docs.ocean.dwavesys.com/projects/binarycsp/en/latest/reference/generated/dwavebinarycsp.ConstraintSatisfactionProblem.fix_variable.html#dwavebinarycsp.ConstraintSatisfactionProblem.fix_variable

"""

print('')
print('Logic gate: 2 by 2 multiplier')
print('=============================')
print('Given virtual qubits a0, a1, b0, b1, c0, c1, c2, c3, c4;')
print('list possible solutions where:')
print('  C = A * B, and C = 9 (c3=1, c2=0, c1=0, c0=1)')
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
    # See these pages for information on embedding:
    # https://docs.dwavesys.com/docs/latest/c_gs_4.html
    # https://docs.dwavesys.com/docs/latest/c_handbook_5.html
else:
    sampler = SimulatedAnnealingSampler()  # simulated quantum annealer
    sampler_embedded = sampler  # we do not need to embed for a simulation

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

For the 2 by 2 multiplier we will use:
  inputs (a0, a1, b0, b1)
  outputs (c0, c1, c2, c3)

For the intermediate variables we will use:
  (and1, and2, and3, and4, xor1, and5, xor2, and6)
However, we will drop some of the intermediate variables because:
  c0 = and2, c1 = xor1, c2 = xor2, c3 = and6

See this image for a graphical view of this circuit:
https://en.wikipedia.org/wiki/Binary_multiplier#/media/File:Binary_multi1.jpg
"""

csp.add_constraint(gates.and_gate(['a0', 'b1', 'and1' ]))  # and(a0, b1) = and1
csp.add_constraint(gates.and_gate(['a0', 'b0', 'c0'   ]))  # and(a0, b0) = c0
csp.add_constraint(gates.and_gate(['a1', 'b0', 'and3' ]))  # and(a1, b0) = and3
csp.add_constraint(gates.and_gate(['a1', 'b1', 'and4' ]))  # and(a1, b1) = and4

csp.add_constraint(gates.xor_gate(['and1', 'and3', 'c1'   ]))  # xor(and1, and3) = c1
csp.add_constraint(gates.and_gate(['and1', 'and3', 'and5' ]))  # and(and1, and3) = and5

csp.add_constraint(gates.xor_gate(['and5', 'and4', 'c2' ]))  # xor(and5, and4) = c2
csp.add_constraint(gates.and_gate(['and5', 'and4', 'c3' ]))  # and(and5, and4) = c3

"""
Now that we have defined the gates for our 2 by 2 multiplier, we need
to fix the output because we want to factor a number. In this case, we
want to factor the number 9, which is 1001 in binary. There are several
ways to fix the number, and each way impacts performance and
correctness differently.

Option 1: (the option we will pick)
For each qubit we want to fix, set a constraint with operator.truth or
operator.not_. "truth" will fix the qubit to 1, and "not_" will fix the
qubit to 0. We are choosing the option because:
- performance and correctness is better than the other options
- it preserves the c3, c2, c1, and c0 labels so we can print them later

Option 2:
Use the fix_variable() function to set the output variables.
For example:
  csp.fix_variable('c3', 1)
  csp.fix_variable('c2', 0)
  csp.fix_variable('c1', 0)
  csp.fix_variable('c0', 1)
I did not like this method because the c3,c2,c1,c0 labels drop out of
the sample.
"""

# We are fixing the output to the number 9, or 1001 in binary
# Here we use "truth" and "not_" operators to set the number we want
# to factor.
csp.add_constraint(operator.truth,['c3'])
csp.add_constraint(operator.not_, ['c2'])
csp.add_constraint(operator.not_, ['c1'])
csp.add_constraint(operator.truth,['c0'])

"""
After we get solutions, the contents of A and B should have factors
of C. In other words, if we fix C = 9, then we expect to see A = 3
and B = 3. (Or, the binary expression: 11 * 11 = 1001)

By adding constraints, we have declared what is and is not acceptible
in solutions. That list of constraints needs to be mapped to a
"binary quadratic model," which is that list of biases and couplings
that were used in the NOT and AND tutorials. The stitch() function
basically generates all of our virtual qubits.
"""

print('Begin stitching...')
bqm = dwavebinarycsp.stitch(csp)
print('Done stitching.')

if (useQpu):
    maxReads = 3000 # use many samples for a QPU
else:
    maxReads = 30   # use few samples for a simulated annealer

"""
Here we ask our sampler for possible solutions. The argument
num_reads sets how many possible solutions we want back in one batch.
If we are using a live QPU, the embedded sampler from above will
automatically map our virtual qubits onto the physical qubits.
The mapping process is called embedding. Keep in mind that automatic
embedding is usually worse than embedding by hand because there is
still a lot to be learned about how to make the best embeddings for
different kinds of problems.
"""

print('Begin sampling...')
response = sampler_embedded.sample(bqm, num_reads = maxReads)
print('Done sampling.')

"""
Now that we have a bunch of possible solutions, we need to sort
through them and check to see which ones are valid. We can get
invalid solutions because the automatic embedding process is
far from perfect. Again, this not necessarily a problem with the
hardware, but more a reflection of how far we need to go to improve
the software tools.

Until we have better embedding tools, we expect more valid solutions
from the simulated annealer. If we want all or many of the valid
solutions, then we need to look into how to make the best embedding
possible. However, sometimes we only need a single valid solution.
If we only need one valid solution, then a mediocre embedding might
be fine.
 
https://docs.ocean.dwavesys.com/projects/dimod/en/latest/reference/generated/dimod.Response.data.html
"""

valid, invalid = 0, 0
for datum in response.data():
    sample, energy, num = datum
    if (csp.check(sample)):
        valid = valid + num
        result = '(' + str(sample['a1']) + str(sample['a0']) + ' * ' + str(sample['b1']) + str(sample['b0']) + ') = '
        result += str(sample['c3']) + str(sample['c2']) + str(sample['c1']) + str(sample['c0'])
        print(result, datum)  # print all valid solutions we find
    else:
        invalid = invalid + num
print(valid, ' valid solutions, ', invalid, ' invalid solutions')
