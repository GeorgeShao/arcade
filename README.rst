Welcome to The ArcadePlus Library!
===================================

ArcadePlus is an easy-to-learn Python library for creating 2D video games.
It is ideal for beginning programmers, or programmers who want to create
2D games without learning a complex framework.

ArcadePlus is built on top of Pyglet and OpenGL.

The ArcadePlus Python library is made by George Shao.

ArcadePlus was forked from Arcade, a Python library made by Paul Vincent Craven.

ArcadePlus is a simpler, more performant Python graphics library than Arcade.

Similar performance improvements have now been integrated into the main Arcade library.

.. image:: https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat
    :target: http://makeapullrequest.com
    :alt: Pull Requests Welcome

.. image:: https://img.shields.io/pypi/l/arcadeplus
    :alt: PyPI - License

How to Install
##############

Type ``pip install arcadeplus`` into your terminal.


Performance Comparison
######################

As seen in the graph below, the ArcadePlus Python library has much better performance than the Arcade Python library.

**Pros:**
Massive frame rate improvements (compared to Arcade v2.3)

UPDATE: As of Arcade v2.4, this depends on your machine specs. It may perform better, worse, or about the same depending on your RAM speed, GPU, and more.

**Cons:**
More memory usage.


**Performance Comparison with Arcade (Arcade 2.3 and earlier):**

.. image:: https://raw.githubusercontent.com/GeorgeShao/arcadeplus/master/arcadeplus/examples/perf_test/original_stress_test_comparison_results.svg
    :alt: Performance Comparison with Arcade (Arcade 2.3 and earlier)

**Performance Comparison with Arcade (After similar changes were integrated into Arcade v2.4):**

.. image:: https://raw.githubusercontent.com/GeorgeShao/arcadeplus/master/arcadeplus/examples/perf_test/stress_test_comparison_results.svg
    :alt: Performance Comparison with Arcade (After similar changes were integrated into Arcade v2.4)


Code Compatibility & Conversion
######################################################
With a few simple changes (listed below), your existing Arcade code will work as intended with ArcadePlus, but an order of magnitude more efficiently.
However, any future ArcadePlus code may not work with Arcade code due to new features and optimizations that may be added.

Method #1
*********
1. Replace any imports such as ``import arcade`` with ``import arcadeplus``
2. Use your IDE's built-in find function to replace all instances of ``arcade.`` with ``arcadeplus.``

Method #2
*********
1. Instead of ``import arcade``, use ``import arcadeplus as arcade``
