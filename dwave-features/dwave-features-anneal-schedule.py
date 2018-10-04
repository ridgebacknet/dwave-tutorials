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

"""
dwave-features-anneal-schedule.py
---------------------------------
  Tutorial for a custom annealing schedule
  This tutorial only works with a live QPU.
  Caution: It is easy to eat up QPU time when experimenting with
  tutorials.

This tutorial covers a fairly sophisticated topic.

Normally, the D-Wave QPU takes about 20µs (that is 0.000020 seconds)
to generate one sample. If you set num_reads=10 in your sampler, then
you can expect to use about 200µs of QPU time.

The example code in this tutorial is for a basic NOT gate. (To
understand how the NOT gate works, see the tutorial in the logic-gates
directory.) We run the NOT gate program three different times, each with
a different annealing schedule. Note that the annealing schedule is only
appropriate for the D-Wave solver. There is no such thing as a custom
anneal schedule for the simulated annealer or for the exact solver.

Requirements
------------

This tutorial can only be run on a live D-Wave QPU.

FAQ
---

What is a quantum annealing schedule?
  There is a toy called a Magic 8-Ball. It is a large ball filled with
  liquid, and it has a window on one side. You gently shake the ball,
  turn it over, and an answer appears. Answers are things like "AS I SEE
  IT YES." Quantum annealing is kind of like that. You shake the ball
  and wait for your answer. Of course I skipped over all the details
  that make it completely unlike a Magic 8-Ball, but that is not the
  point. The point is that you get to decide how long you shake the
  Magic 8-Ball, and somehow that might affect the outcome. Likewise,
  the quantum annealing schedule is essenstially the rate at which
  energy is applied to the quantum system, in an effort to affect the
  outcome. To understand the hows and whys requires far more explanation
  than this tutorial.

Why would I change the annealing schedule?
  A good answer needs to go into the physics of what is happening
  during a quantum anneal. The D-Wave documentation is the best place
  to learn about that. From a programming perspective, there are some
  problems that are solvable, but require many samples to find an
  acceptable solution. Those kinds of problems sometimes can benefit
  from a pause in the anneal cycle. Ideally, that pause should occur
  when an incorrect solution is almost as probable as a correct
  solution. There are other times when a pause (or acceleration) in the
  annealing cycle can produce better results, but investigating those
  details is an area of active research.

References
----------

- https://docs.dwavesys.com/docs/latest/c_qpu_0.html#annealing-controls
- https://en.wikipedia.org/wiki/Quantum_annealing
- https://en.wikipedia.org/wiki/Adiabatic_quantum_computation
- Tanaka, S., Tamura, R., and Chakrabarti, B.
  *Quantum Spin Glasses, Annealing and Computation.*
  Cambridge University Press. 2017.

"""

# The example code uses different annealing schedules. We definte three
# different functions, each returning a list suitable for use as a
# custom annealing schedule.
#
# A custom annealing schedule is a list of pairs. The first number in
# the pair is the time (in microseconds), and the second number is the
# percentage of the anneal. (The anneal goes from 0.0 to 1.0, or 0% to
# 100%.)
# Important: Neither the time nor the anneal percentage can go backwards
# in the schedule.

# Quench the anneal after 5µs. This is a very quick anneal. The anneal
# cycle normally lasts 20µs.
def anneal_sched_custom_1():
    return (
        (0.0, 0.0),  # Start the anneal (time 0.0) at 0.0 (min)
        (5.0, 1.0)   # After 5µs, set the anneal setting to 100% (max)
    )

# Quickly ramp up from 0µs to 5µs.
def anneal_sched_custom_2():
    return (
        (0.0, 0.0),  # Start the anneal (time 0.0) at 0.0 (min)
        (5.0, 0.5),  # After 5us, set the anneal setting to 50%
        (20.0, 1.0)  # After 20us, set the anneal setting to 100% (max)
    )

# A custom anneal schedule can have up to four points.
def anneal_sched_custom_3():
    return (
        (0.0, 0.0),   # Start everything at 0
        (1.0, 0.80),  # Quickly ramp up to 80% anneal at 1µs
        (19.0, 0.81), # From 1µs to 19µs, slowly go from 80% to 81%.
        (20.0, 1.0)   # End the full anneal at 20µs
    )

print('Boolean NOT Gate with Default Annealing Schedule')
sampler = DWaveSampler()
# We put a small bias for qubit 0 to see if the annealing schedule
# makes a difference in the distribution of solutions.
Q = {(0, 0): -1.1, (0, 4): 0, (4, 0): 2, (4, 4): -1}

response_1 = sampler.sample_qubo(Q, anneal_schedule=anneal_sched_custom_1(), num_reads=1000)
response_2 = sampler.sample_qubo(Q, anneal_schedule=anneal_sched_custom_2(), num_reads=1000)
response_3 = sampler.sample_qubo(Q, anneal_schedule=anneal_sched_custom_3(), num_reads=1000)

print('Anneal schedule 1:')
for sample, energy, num_occurrences in response_1.data():
    print(sample, "Energy: ", energy, "Occurrences: ", num_occurrences)
print('Anneal schedule 2:')
for sample, energy, num_occurrences in response_2.data():
    print(sample, "Energy: ", energy, "Occurrences: ", num_occurrences)
print('Anneal schedule 3:')
for sample, energy, num_occurrences in response_3.data():
    print(sample, "Energy: ", energy, "Occurrences: ", num_occurrences)

"""
If we run it enough times, we can see some anomalies in the output.
Sample output:

$ python3 dwave-features-anneal-schedule.py
Boolean NOT Gate with Default Annealing Schedule
Anneal schedule 1:
{0: 1, 4: 0} Energy:  -1.1 Occurrences:  763
{0: 0, 4: 1} Energy:  -1.0 Occurrences:  236
{0: 1, 4: 1} Energy:  -0.10000000000000009 Occurrences:  1
Anneal schedule 2:
{0: 1, 4: 0} Energy:  -1.1 Occurrences:  768
{0: 0, 4: 1} Energy:  -1.0 Occurrences:  232
Anneal schedule 3:
{0: 1, 4: 0} Energy:  -1.1 Occurrences:  727
{0: 0, 4: 1} Energy:  -1.0 Occurrences:  272
{0: 0, 4: 0} Energy:  0.0 Occurrences:  1

"""
