README for dwave-tutorials Repository
=====================================

This repository contains various tutorials for programming the D-Wave
Systems quantum computer. The D-Wave is a real quantum computer that
you can program today. These tutorials are not meant as a replacement
for the official D-Wave documention; these tutorials are meant to give
example code and comments for some problems that can be solved on a
D-Wave quantum computer.

Who are these tutorials for?
----------------------------

These tutorials are for software developers that know Python.
The focus is on programming the D-Wave, with little to no theory. Most
of what has been written about quantum computing has been for either
physicists or computer science theoreticians -- we're talking really,
really deep stuff. I am trying to present quantum computing without the
formality that is normally associated with it. My hope is that an
average software developer will be able to learn from these tutorials.

Keep in mind that the tool chain for the D-Wave is not anywhere near
as mature as you may be used to. The hardware technology is new and
the software stack is trying to catch up. On the bright side, there is
an awesome opportunity for people to contribute to the tool ecosystem.

Some of the tutorials are based on D-Wave documentation, any errors
in these tutorials are mine alone.

All feedback is welcome. If you would like to see tutorials on a
specific subject, please let me know.

Requirements
------------

To use these tutorials you need:

- Python
- pip
- dwave-ocean-sdk

Here is how to get started:

``
pip install dwave-ocean-sdk
``

To run a tutorial:

``
python <tutorial_name>.py
``

Some very useful documentation is online:

- https://docs.ocean.dwavesys.com/en/latest/index.html
- https://docs.dwavesys.com/docs/latest/index.html
- https://docs.dwavesys.com/docs/latest/c_handbook_8.html

Open source D-Wave repositories are also online:

- https://github.com/dwavesystems

The D-Wave Systems LEAP portal is online:

- https://cloud.dwavesys.com/leap/

What good is quantum computing?
-------------------------------

In a nutshell, quantum computing is what will get us to those really
cool science fiction technologies like easy space travel, replicated
food, and invisibility cloaks. There are countless potential
breakthroughs waiting for computers with enough horsepower to solve
extremely difficult problems. Those computers will not work like
traditional computers, so someone needs to learn how to program in new
ways.

Quoting from some Princeton class notes on intractability, here is a
list of the types of problems that quantum computing can help with:

- Aerospace engineering: Optimal mesh partitioning for finite elements
- Biology: Phylogeny reconstruction
- Chemical engineering: Heat exchanger network synthesis
- Chemistry: Protein folding
- Civil engineering: Equilibrium of urban traffic flow
- Economics: Computation of arbitrage in financial markets with friction
- Electrical engineering: VLSI layout
- Environmental engineering: Optimal placement of contaminant sensors
- Financial engineering: Minimum risk portfolio of given return
- Game theory: Nash equilibrium that maximizes social welfare
- Mechanical engineering: Structure of turbulence in sheared flows
- Medicine: Reconstructing 3d shape from biplane angiocardiogram
- Operations research: Traveling salesperson problem
- Physics: Partition function of 3d Ising model
- Politics: Shapley-Shubik voting power
- Recreation: Versions of Sudoko, Checkers, Minesweeper, Tetris
- Statistics: Optimal experimental design

You can read the Princeton notes on hard computer science problems here:
https://www.cs.princeton.edu/courses/archive/spring13/cos423/lectures/08IntractabilityII.pdf

Caution: Be careful with your QPU time.
---------------------------------------

You can run most of the tutorials using either a simulated annealing
sampler or using a live D-Wave quantum processing unit (QPU). Some
people have direct access to a D-Wave computer through a business,
university, or research organization. However, most people will access
a D-Wave computer through the D-Wave Systems cloud service called LEAP.
Therefore, your QPU time may be limited. If you have limited QPU time,
it is better to go through the tutorials using the simulated annealer,
and then use a live D-Wave for really tough problems.

When possible, each tutorial defaults to using a simulated annealer.

About the D-Wave
================

What is a D-Wave?
-----------------

D-Wave Systems is a company that makes a computer called the D-Wave. The
D-Wave is a quantum computer that uses quantum annealing to solve
extremely difficult problems. The D-Wave is real, it works, and it can
be used to solve meaningful real-world problems.

Why am I excited about programming the D-Wave?
----------------------------------------------

Good programmers love to learn new technologies. Quantum computing is
a new technology that is poised to take off and change the world
dramatically. D-Wave Systems has opened up access to their latest
quantum computer to let everyone learn and experiment to see what is
possible. The best part is that the D-Wave is mature enough that it
can be used to solve real-world problems.

I have been programming computers since CPUs were 8 bits, anything
faster than 1MHz was really fast, and 16,384 bytes was a lot of memory.
Computers completely transformed the way all of civilization works. I
feel lucky to be alive (and still programming) today, because we are
about to witness another similar transformation. The D-Wave is the
first quantum computer to reach the point where it is useful enough
to disrupt the field of computing. Having cloud access to a computer
like that is very exciting.

Is the D-Wave really a quantum computer?
----------------------------------------

Yes. The D-Wave definitely uses quantum effects to perform calculations,
and you can use it to solve meaningful problems today. Keep in mind that
the D-Wave is more efficient than classical computers only when it is
solving very hard problems. In theory, certain quantum computers
(including future D-Wave models) are more efficient. Unfortunately,
theoretical computers are just that -- they do not yet exist.

What is the catch?
------------------

The catch is that we are right at the beginning of practical quantum
computing. No early technology is perfect, and the D-Wave is no
exception. Many other successful technologies had warts when they
started - modern 8-bit CPUs, RAM (that's random access memory),
monitors, printers, compilers (like C or C++), interpreters (like
Perl and Python), telephones, and so on. So, it's not perfect, but it
is useable, useful, scalable, relatively easy to program, and online
and working today. I have every reason to believe that the D-Wave
performance will improve significantly over the next few years.

Here are some references for the technology behind the D-Wave:

- https://www.dwavesys.com/resources/publications
- https://docs.ocean.dwavesys.com/en/latest/index.html
- https://docs.dwavesys.com/docs/latest/index.html
- https://en.wikipedia.org/wiki/Quantum_annealing
- https://en.wikipedia.org/wiki/Adiabatic_quantum_computation
- Tanaka, S., Tamura, R., and Chakrabarti, B.
  *Quantum Spin Glasses, Annealing and Computation.*
  Cambridge University Press. 2017.

The issues surrounding theoretical performance are both subtle and
complex. It is often difficult to understand the relationship between
what the theoreticians say and what the practitioners say. If you want
to jump into discussions on quantum performance, then at a minimum,
I would recommend working through the book by Tanaka, Tamura, and
Chakrabarti to understand the deeper issues regarding theoretical and
practical performance.

Who writes these tutorials?
===========================

Hi! I'm Thomas Phillips, the CTO at Ridgeback Network Defense. I make
cybersecurity "stuff." My vision is that eventually (soon, I hope) all
assets (digital and physical) will be protected aggressively by
autonomous, intelligent, self-aware systems. We have already started
down this road with Ridgeback Hunter, and I am constantly looking for
both advanced technologies and the brightest and most talented people to
help make that vision a reality. I think quantum computing may be
instrumental in realizing the vision. Therefore, I want as many people
as possible ready to take the plunge with quantum computing. I work on
these tutorials in my spare time; please forgive me if anything goes
out of date.

Beyond any work related goals, I hope that these tutorials can inspire
young computer enthusiasts, igniting a passion for this revolutionary
new technology we call quantum computing. I can remember many decades
ago when someone from Motorola answered a letter I wrote, asking for
information on the 6809E 8-bit microprocessor. The manuals and documents
they sent me were like mystical arcane tomes that filled me with wonder,
awe, and boundless curiousity. I would consider it a great
accomplishment if I can inspire anyone to pursue quantum computing with
that same kind of fervent enthusiasm.

Finally, I definitely want to acknowledge the awesome folks at D-Wave
Systems. A lot of the material is based on their documentation, and I
try to provide links back to D-Wave documentation when possible.
D-Wave's openness and eagerness to share and educate has made these
tutorials possible. Nothing truly great is accomplished by one person;
the hard work by the folks at D-Wave Systems has allowed us all to move
forward into a world with real quantum computers.
