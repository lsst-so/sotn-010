################################################################
Comparison of Peak Memory Usage Among Conda-Compatible Tools
################################################################

.. abstract::

   An experiment comparing the peak memory usage of Conda-compatible tools during local and continuous-integration builds.

This technote describes an experiment comparing the peak memory usage of Conda-compatible tools.

Our current setup runs Conda builds every weekday.
When we need to test two Python versions, we must build twice.
This increases build time and may increase memory pressure on the Jenkins nodes.

This experiment has two goals:

a) verify whether conda-build produces a high memory load; and
b) compare alternative tools to determine whether they reduce memory usage.

The measurements cover local tool runs, CI pipeline runs, and solver-specific conda-build runs.
Each local test records elapsed time and maximum resident set size for three samples.
The CI measurements compare different test runners, execution modes, and package builders.
The solver comparison records elapsed time and maximum resident set size for libmamba and experimental Rattler configurations.

The first table compares local build memory usage across conda-build, Nox, Pixi, and rattler-build.
In these tests, conda-build consistently uses the most memory.
Nox, using Conda as its virtual-environment backend, also has consistently high memory usage.
Pixi and rattler-build use less memory and complete the tests in less time.

The second table shows peak memory usage during CI pipeline runs.
It compares how each test runner, execution mode, and package builder affects the build environment.
The third table compares memory usage between the libmamba and experimental Rattler solvers.

The results across all three tables suggest that Conda-based workflows have a higher memory cost in these tests, regardless of the solver used.
Switching to Rust-based tooling could produce substantial memory savings and reduce resource pressure on Jenkins CI.

.. csv-table:: Local Build Memory Usage
   :file: _static/test-memory.csv
   :header-rows: 1

.. csv-table:: CI Pipeline Memory Usage
   :file: _static/ci-pipeline-memory.csv
   :header-rows: 1

.. csv-table:: Conda Solver Memory Usage
   :file: _static/conda-solver-memory.csv
   :header-rows: 1
