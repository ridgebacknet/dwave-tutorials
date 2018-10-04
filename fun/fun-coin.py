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

import time
from dwave.system.samplers import DWaveSampler
from neal import SimulatedAnnealingSampler
from dwave.system.composites import EmbeddingComposite

useQpu = False   # change this to use a live QPU
trials = 5000   # How many trials in the coin flipping experiment

"""
fun-coin.py
-----------
  Tutorial for flipping a coin.
  This tutorial covers timing and probability distributions.
  To use a live QPU, set useQpu to True.

Quantum computers are wonderful at generating random numbers.
Let's flip some coins!
"""

print('')
print('Coin Flipperama!')
print('================')
print('     ??????     ')
print('    ??    ??    ')
print('   ??  ??  ??   ')
print('   ??  ??  ??   ')
print('    ??    ??    ')
print('     ??????     ')
print('Flip a bunch of coins and show the distribution.')
print('')

# At the top of this file, set useQpu to True to use a live QPU.
if (useQpu):
    sampler = DWaveSampler()
    # We need an embedding composite sampler because not all qubits are
    # working. A trivial embedding lets us avoid dead qubits.
    sampler = EmbeddingComposite(sampler)
else:
    sampler = SimulatedAnnealingSampler()

# Initialize a binary quadratic model.
# It will use 2000 qubits. All biases are 0 and all couplings are 0.
bqm = {}       # binary quadratic model
distrib = {}   # distribution

msg = 'How many coins do you want to flip at the same time?'
try:
    coins = raw_input(msg)
except:
    try:
        coins = input(msg)
    except:
        print('I give up! Why can\'t I ask you questions?')
        max_coins = 50

try:
    max_coins = int(coins)
except:
    print('That is a weird number. I am going with 50.')
    max_coins = 50

if (max_coins > 2000):
    print('Too many coins! I am only flipping 2000 at a time.')
    max_coins = 2000

if (max_coins < 1):
    print('Too few coins! I am going to flip one coin at a time.')
    max_coins = 1
    
for i in range(0, max_coins):
    bqm[(i,i)] = 0  # indicate a qubit will be used
    distrib[i] = 0  # initialize the distribution to all 0
distrib[max_coins] = 0  # We need one extra slot for the distribution

print('Okay, for each trial I am going to flip %d coins' % max_coins)
print('and I will repeat this for %d trials.' % trials)
print('Next, I will display a distribution of how many coins came up heads.')
print('This is very exciting, don\'t you think?')
print('')
print('DON\'T BLINK!')
print('')

start = time.time()
response = sampler.sample_qubo(bqm, num_reads=trials)
end = time.time()
total = (end - start)

try:
    qpu_access_time = response.info['timing']['qpu_access_time']
except:
    qpu_access_time = 0
    print('QPU access time is not available. This makes me sad.')

print('Whew! That was really tough. It took me '+'{:10.4f}'.format(total)+' seconds to flip '+'{:d}'.format(trials * max_coins)+' coins.')
print('Of all that time, the QPU was used for '+'{:10.8f}'.format(qpu_access_time/1000000)+' seconds.')
print('')
print('Give me a moment to sort out these results...')

# This is a very slow, brute force nested loop.
for datum in response.data():  # for each series of flips
    n = 0
    for key in datum.sample:   # count how many heads or tails
        if (datum.sample[key] == 1):
            n += 1
    distrib[n] += 1

# Determine the maximum in our distribution array
# so we can normalize the widths of the bars.
max_count = 0
for i in range(0, len(distrib)):
    if (distrib[i] > max_count):
        max_count = distrib[i]

print('Ah, here we go. Here is your distribution for')
print('the total number of heads per trial:')
print('---------------------------------------------')
print('')

# Print out the distribution!
width = 72  # the maximum width of a bar
for i in range(0, len(distrib)):
    print(i, 'x' * int( round( 60 * (distrib[i] / max_count) ) ) )

print('')
print('Wasn\'t that fun? Have nice day! :-)')

"""
Here are some Sample timing metrics available from a sampler response.
All times are in µs (1µs = 0.000001s).

{'timing': {
    'total_real_time': 827389,
    'qpu_access_overhead_time': 2487,
    'anneal_time_per_run': 20,
    'post_processing_overhead_time': 360,
    'qpu_sampling_time': 819800,
    'readout_time_per_run': 123,
    'qpu_delay_time_per_sample': 21,
    'qpu_anneal_time_per_sample': 20,
    'total_post_processing_time': 2185,
    'qpu_programming_time': 7589,
    'run_time_chip': 819800,
    'qpu_access_time': 827389,
    'qpu_readout_time_per_sample': 123
  }
}

If you want to know how much QPU time your operation will take, total,
calculate:
num_reads * (readout_time_per_run + qpu_delay_time_per_sample + qpu_anneal_time_per_sample)

In the above sample timing, the total QPU time was 827389µs for
5000 samples. That is 819800µs for the the samples, and 7589µs QPU overhead.
That is 163.96µs per sample, or (123µs + 21µs + 20µs) per sample.
So, the books balance.

Here is sample output from flipping 10 coins at a time.
QPU time is 0 because it was run with a simulated annealer.

Coin Flipperama!
================
     ??????     
    ??    ??    
   ??  ??  ??   
   ??  ??  ??   
    ??    ??    
     ??????     
Flip a bunch of coins and show the distribution.

How many coins do you want to flip at the same time? 10
Okay, for each trial I am going to flip 10 coins
and I will repeat this for 5000 trials.
Next, I will display a distribution of how many coins came up heads.
This is very exciting, don't you think?

DON'T BLINK!

QPU access time is not available. This makes me sad.
Whew! That was really tough. It took me     0.1940 seconds to flip 50000 coins.
Of all that time, the QPU was used for 0.00000000 seconds.

Give me a moment to sort out these results...
Ah, here we go. Here is your distribution for
the total number of heads per trial:
---------------------------------------------

0 
1 xxx
2 xxxxxxxxxxx
3 xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
4 xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
5 xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
6 xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
7 xxxxxxxxxxxxxxxxxxxxxxxxxxxxx
8 xxxxxxxxxx
9 xxx
10 

Wasn't that fun? Have nice day! :-)

"""

