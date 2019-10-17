.. _Principles:

Principles of Flight Data Processing
====================================

Flight Data Characteristics
---------------------------

POLARIS is a data analysis suite designed specifically to perform computations on recorded flight data.
Flight data recorded on aircraft Flight Data Recorders (FDRs) has specific characteristics which we have to
address in such a system.

The first characteristic of flight data is that the data is recorded in a compressed binary format. The
accuracy of some parameters is degraded to reduce the length of the recorded binary number.
Therefore, an initial step in processing is to convert the binary values into their engineering units—and
this is not a trivial process.
Different aircraft types, variants and even recording equipment manufacturers have introduced a multitude of
data formats; the permutations of which run into the hundreds.
Each needs a specific set of decoding algorithms and, while many features can be standardised, it is
often necessary to develop data format-specific algorithms to cater for special cases.
This is indeed an area where special cases are common!

The second characteristic of flight data is that each parameter is sampled at a different point in time
with varying sample rates and latencies. This is an underlying signal processing problem in all
flight data systems which has to be addressed to process data accurately.

Data Latency
------------

When computing the sample point for a conventional parameter, the time from the start of the data frame is given by::

 T = n.dt

Where n is the number of samples from the start of the frame and dt is the sample interval.

Digital (ARINC 429) parameters can exhibit a latency between the moment the measurement was taken and when it was recorded into a frame. The latency is a function of the digital data transfer process.

For a parameter with latency, the time from the start of the data frame is given by::

 T = n.dt – L

Where L is the latency.

It follows that parameters with large latencies sampled close to the beginning of the frame could have been sampled during the
preceding frame.

A typical value of L might be 50 mS. With data sampled at 256 wps, this corresponds to shifting a data point 1/20th
second or 13 samples earlier than its position implies.


Computing With Data Latency
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. The problem of computing in the presence of data latency is illustrated in the diagram below. Here two parameters
   with differing sample rates and latency have been represented by 'a' and 'b' and a calculation has been performed
   at times representing 0, 1, 2 seconds into the data. This is typical of analysis systems that perform periodic computations.

   The computed values, represented by the green squares, do not lie on the correct result path and these errors
   can build surprisingly rapidly. As an example, FDS had one algorithm for computing the takeoff where the compuation lag
   was so bad that the radio altimeter readings had reached almost 70ft at the point of computed takeoff.

   It is possible to keep such errors under control, but it would be better not to have such errors in the first place.

By default FlightDataAnalyzer calculations are exact in time for the primary parameter in a computation and accept an interpolated
estimate of the secondary parameter(s).

.. image:: _images/alignment_plot.png

One mathematical issue here is that the results are non-communtative. That is to say::

    a + b != b + a
and::

    a * b != b * a

We will see later how this affects the implementation of the algorithms, but suffice to say for now that the
implementation takes the effort away from the programmer and end users will as a result receive more accurate answers.

.. _aligning:

Aligning of parameters
----------------------

Matrix computation generally requires datasets of the same shape:

    >>> np.arange(10) * np.arange(20)
    Traceback (most recent call last):
      File "<string>", line 1, in <fragment>
    ValueError: operands could not be broadcast together with shapes (10) (20)


Aligning parameters allows us to create arrays which have the same shape.
Aligning also solves the problem of time differences between parameters. An aligned parameter's data is linearly interpolated to produce accurate values relative to the parameter it is aligned to.


Frequency
~~~~~~~~~

Flight Data parameters which are sampled at different frequencies will have a
different number of samples for a given flight duration. The
FlightDataAnalyzer is able to increase and decrease the sample rate of a
given parameter to ensure the matrix arrays are of the same shape.

When increasing sample rate, linear interpolation is used to gain a
statistically more probable value of the recorded parameter between the
previous and next recorded samples.

.. Offset
   ~~~~~~

   As valids To ensure the accuracy of the data is maintained...
   of multiple parameters is best performed with Align of all dependencies to the first available dependency


Discrete and Multi-state parameters
-----------------------------------

Aligning parameter arrays with linear interpolation is not suitable in all cases.

Discrete and Multi-state parameters record integer values which represent states. Linear interpolation is not applied to these parameters during alignment. Instead, the values are repeated when aligned to a parameter with a higher sample rate. If the alignment parameter has a lower sample rate, the array will be resampled at the alignment frequency. Typically, parameters are aligned to the highest available sample rate to avoid data loss.


Automatic Alignment (Default)
-----------------------------

By default, all dependencies will be aligned to match the frequency and offset of the first available dependency.

.. code-block:: python

   class DerivedFromFlap(KeyPointValueNode):

       def derive(self, aileron=P('Aileron'), flap=M('Flap'), liftoffs=KTI('Liftoff')):
           ...

In the above example, if all dependencies are available, both Flap and Liftoff will be aligned to have the same frequency and offset as Aileron. While
Flap's parameter data will be linearly interpolated, Aileron's parameter data will not be modified. Generally it is
preferable to align to parameter nodes where possible as the alignment of indices within other node types is a less
significant modification than interpolating parameter data values. The most important dependency should be listed first
to maintain the original values of whichever input is most important for the node's calcuation. For example, if the above
node is creating Key Point Values which sample Flap rather than Aileron, it would be preferable for Flap to be its
first dependency:

.. code-block:: python

   class DerivedFromFlap(KeyPointValueNode):

       def derive(self, flap=M('Flap'), aileron=P('Aileron'), liftoffs=KTI('Liftoff')):
           ...


Manual Alignment
----------------

Another instance where linear interpolation would be detrimental is stepped parameters such as Flap. Stepped parameters are similar to Multi-state parameters in that they record a discrete number of integer values.

.. image:: _images/align_flap.png

Alignment of a node's dependencies can be disabled for a Node by assigning the static class attribute `align` to be False.

.. code-block:: python

   class DerivedFromFlap(DerivedParameterNode):
       align = False

       def derive(self, aileron=P('Aileron'), flap=M('Flap')):
           ...

All dependencies can be aligned to a specific frequency and/or offset by assigning the static class attributes `align_frequency` and `align_offset`.

.. code-block:: python

   class DerivedFromFlap(DerivedParameterNode):
       align_frequency = 2
       align_offset = 0.5

       def derive(self, aileron=P('Aileron'), flap=M('Flap')):
           ...

