# SRControl: Linux CGroups made easy

Goal: Build an easy to use API for cgroups that can be used for:

TODOS:

1. Segementing routines and subroutines into cgroups
* Data privacy, namespacing
* Auto restart for routines that die
* Auto scaling for routines that die

2. Metrics for segmented routines
* Bubble up memory, IO, cpu usage statistics for use with monitoring libraries
* React to metrics intelligently

Requires:
* Python 3.6+
* CGroups V2 ( And so, privilege )
