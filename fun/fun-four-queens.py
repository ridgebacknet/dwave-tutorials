'''
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
'''

import time
from dwave.system.samplers import DWaveSampler
from neal import SimulatedAnnealingSampler
from dwave.system.composites import EmbeddingComposite
import dwavebinarycsp
import dwavebinarycsp.factories.constraint.gates as gates
import operator

useQpu = False   # change this to use a live QPU
samples = 1000   # Default number of samples

'''
fun-four-queens.py
------------------
  Tutorial for four-queens puzzle.
  To use a live QPU, set useQpu to True.

The four-queens puzzle is the archetypal constraint satisfaction problem.
Let's see if we can mix things up a bit.

The constraints technique used in this tutorial was based on Dr. Haiou
Shen's web page on n-queens and SAT solvers:
- https://sites.google.com/site/haioushen/search-algorithm/solvean-queensproblemusingsatsolver

'''

# At the top of this file, set useQpu to True to use a live QPU.
if (useQpu):
    sampler = DWaveSampler()
    # We need an embedding composite sampler because not all qubits are
    # working. A trivial embedding lets us avoid dead qubits.
    sampler = EmbeddingComposite(sampler)
else:
    sampler = SimulatedAnnealingSampler()

# Every time I try to type "print," my fingers type "printf."
# So, I am going to use "p" instead!
p = print

# We will want to ask input now and then; Python 2 and Python 3 handle
# differently.
try:
    input # We want to use the input() function
except:
    input = raw_input # Python 2 has a raw_input() function

# The mysterial Q variable will be a lookup for drawing on the screen.
Q = {}
Q[0] = '*'
Q[1] = 'Q'

p('''

   ##  ##  ##  ##
    ############
     ##########
       ######
       ######
     ##########
     ##########
       ######
       ######
       ######
       ######
       ######
       ######
    #############
 ##################
####################


Hi there! We will attempt to solve the four-queens puzzle.
Let's break it down into steps.
''')

input('Press enter to get started!\n>')

p('''
Step 1
------
Assume we have a row of four spaces, and exactly one queen can be
placed on any of those spaces. What are the possible solutions?

Our board looks like this:

  x1 x2 x3 x4

Our solutions will be four-bit strings, with a 1 showing where the
queen is.
''')

'''
We will be using some logic. Here are the notations we will use:

  ===   is equivalent to
  |     logical or
  &     logical and
  !     logical not
  ==    is equal to
  true  true
  1     true
  false false
  0     false

For our first problem, we have a row of elements labeled:

  x1 x2 x3 x4

If there must be exactly one element set to true, then:

  x1 | x2 | x3 | x4 == true

This one is tricky because we need a four-way OR function.
'''

# function that returns a 4-way logical or
def or4(i0, i1, i2, i3):
    return (i0 or i1 or i2 or i3)

'''
Next, there must be no more than one element set to true. One way to do
this is:

  !x1 | !x2 == 1

This term works for a constrant as long as x1 and x2 are not both 1.
(!1 | !1 is 0.) A NAND gate would be equivalent and less verbose.
'''

# We add this helper function because the csp gates class is missing
# NAND, the most universally awesome gate on the planet.
def nand(in0, in1):
    return not (in0 and in1)

'''
With our new NAND function we can constrain the elements so that only
one element can be set at a time.

  NAND(x1,x2) == 1
  NAND(x1,x3) == 1
  NAND(x1,x4) == 1
  NAND(x2,x3) == 1
  NAND(x2,x4) == 1
  NAND(x3,x5) == 1

CAUTION:
If you are using a live QPU, it is possible that the stitch() and
embedding will result in a physical configuration of qubits that does
not provide any solutions. This is a problem with the tool chain, not
the hardware. There is a great opportunity for someone to create a
constraint solver plus embedder that prevents embeddings without
solutions.

Let's run our single-row solver and see how it works.
'''

csp = dwavebinarycsp.ConstraintSatisfactionProblem(dwavebinarycsp.BINARY)

# At least one qubit must be set
csp.add_constraint(or4, ['x1', 'x2', 'x3', 'x4'])

# No more than one qubit can be set
csp.add_constraint(nand, ['x1', 'x2'])
csp.add_constraint(nand, ['x1', 'x3'])
csp.add_constraint(nand, ['x1', 'x4'])
csp.add_constraint(nand, ['x2', 'x3'])
csp.add_constraint(nand, ['x2', 'x4'])
csp.add_constraint(nand, ['x3', 'x4'])

bqm = dwavebinarycsp.stitch(csp)
response = sampler.sample(bqm, num_reads = samples)

# aggregate the results
answers = {}
valid, invalid = 0, 0
for datum in response.data():
    sample, energy, num = datum
    if (csp.check(sample)):
        valid = valid + num
        result = ''
        for i in range(1,5):
            result += str(sample['x'+str(i)])
        try:
            answers[result] += num
        except:
            answers[result] = num
    else:
        invalid = invalid + num

for key in answers:
    p(key, '('+str(answers[key])+' times)\n')
p(valid, ' valid solutions, ', invalid, ' invalid solutions')

p('''
Step 2
------
So far, so good.

If you used a live QPU and saw no or too few solutions, then you
probably had an unlucky embedding. Your hardware is okay -- the issue
is a flaw in the tool chain.

Next we will expand the board to be a 4 by 4 grid. We will use the same
kinds of constraints and see if we can place four queens.
''')
input('Press enter to try the four-queens problem.\n>')

csp = dwavebinarycsp.ConstraintSatisfactionProblem(dwavebinarycsp.BINARY)

'''
This time we are using a grid that looks like this:

x11 x12 x13 x14
x21 x22 x23 x24
x31 x32 x33 x34
x41 x42 x43 x44

We will start off setting constraints by hand, but this will get tedious
after a while.
'''

# At least one qubit must be set in each row.
csp.add_constraint(or4, ['x11', 'x12', 'x13', 'x14'])
csp.add_constraint(or4, ['x21', 'x22', 'x23', 'x24'])
csp.add_constraint(or4, ['x31', 'x32', 'x33', 'x34'])
csp.add_constraint(or4, ['x41', 'x42', 'x43', 'x44'])

# You should start noticing a pattern. We will start automating
# the constraints.
# No more than one qubit can be set in each row.
# We process one row at a time.
for row in (1, 2, 3, 4):
    for col in (1, 2, 3):
        for i in range(col+1, 5):
            csp.add_constraint(nand, ['x'+str(row)+str(col), 'x'+str(row)+str(i)])

# No more than one qubit can be set in each column.
# We process one column at a time.
for col in (1, 2, 3, 4):
    for row in (1, 2, 3):
        for i in range(row+1, 5):
            csp.add_constraint(nand, ['x'+str(row)+str(col), 'x'+str(i)+str(col)])

'''
Since we are placing queens, and queens can move diagonally, we need
some diagonal constraints. This is what one diagonal constraing would
look like if it was placed by hand:

  csp.add_constraint(nand, ['x11', 'x22'])
  csp.add_constraint(nand, ['x11', 'x33'])
  csp.add_constraint(nand, ['x11', 'x44'])
  csp.add_constraint(nand, ['x22', 'x33'])
  csp.add_constraint(nand, ['x22', 'x44'])
  csp.add_constraint(nand, ['x33', 'x44'])

There are 10 diagonals in a 4x4 grid, so let's automate the constriants.

The diagonal_se_constraint_4x4 function iterates over diagonals and sets
NAND constraints. (Only one element is allowed per diagonal.)
Notice that this is a sloppy function -- we brute force the inner and
outer loop, and use an if to see if we are still in bounds. This is not
efficient, but it makes the code much easier to understand.
By the way, "se" is southeast.
'''
def diagonal_se_constraint_4x4(csp, row, col):
    for a in range(0, 5):
        for b in range(a + 1, 5):
            if ( ((row + b) <= 4) and ((col + b) <= 4) ):
                csp.add_constraint(nand, ['x'+str(row + a)+str(col + a), 'x'+str(row + b)+str(col + b)])

# Set the constraints for the 5 southeast traveling diagonals
diagonal_se_constraint_4x4(csp, 3, 1)
diagonal_se_constraint_4x4(csp, 2, 1)
diagonal_se_constraint_4x4(csp, 1, 1)
diagonal_se_constraint_4x4(csp, 1, 2)
diagonal_se_constraint_4x4(csp, 1, 3)

# As the kids would say at the amusement park,
# "Let's do it again! Again!"
def diagonal_sw_constraint_4x4(csp, row, col):
    for a in range(0, 5):
        for b in range(a + 1, 5):
            if ( ((row + b) <= 4) and ((col - b) >= 1) ):
                csp.add_constraint(nand, ['x'+str(row + a)+str(col - a), 'x'+str(row + b)+str(col - b)])

# Set the constraints for the 5 southwest traveling diagonals
diagonal_sw_constraint_4x4(csp, 1, 2)
diagonal_sw_constraint_4x4(csp, 1, 3)
diagonal_sw_constraint_4x4(csp, 1, 4)
diagonal_sw_constraint_4x4(csp, 2, 4)
diagonal_sw_constraint_4x4(csp, 3, 4)

bqm = dwavebinarycsp.stitch(csp, min_classical_gap=3.2)
'''
Hey! What is a min_classical_gap?
    We are telling the stitch function that we want to optmize for
    accuracy. That is, when our solution gets embedded on a live D-Wave,
    we want to increase the probabilty that the QPU will settle into a
    valid solution.

Why are we using it?
    With a gap of 2.0, the embedding is too poor quality to find
    solutions without a lot -- and I mean A LOT -- of samples.

The default for min_classical_gap is 2.0. If you go crazy and try some
large number -- well, I do not know what will happen. Caveat utilitor.
'''
response = sampler.sample(bqm, num_reads = samples)

# aggregate the results
answers = {}
valid, invalid = 0, 0
for datum in response.data():
    sample, energy, num = datum
    if (csp.check(sample)):
        valid = valid + num
        # result = ''
        result = '+-+-+-+-+\n'
        for row in range(1,5):
            for col in range(1,5):
                # We use our cool Q variable to draw
                result += '|'+Q[sample['x'+str(row)+str(col)]]
            result += '|\n'
            result += '+-+-+-+-+\n'
        try:
            answers[result] += num
        except:
            answers[result] = num
    else:
        invalid = invalid + num

for key in answers:
    p(key, '('+str(answers[key])+' times)\n')
p(valid, ' valid solutions, ', invalid, ' invalid solutions')


if (valid == 0):
    p('Hmmm... Looks like we struck out. Try again and better luck next time.')
elif ((valid / (valid + invalid)) < 0.1):
    p('Not a huge number of valid solutions, but hey, it worked!')
else:
    p('Wow! Look at those solutions!')

p('''
Now that you have gone through a four-queens tutorial, how about if
you expand it to make an eight-queens program? Or maybe even an n-queens
program?

One word of caution:
The hardest part of working with a live QPU is finding an optimal
embedding. Until we get some awesome optimizers, the tool chain will
only get you so far before you have to worry about doing a few
optimizations by hand.

That's it for now. Have a nice day!
''')

