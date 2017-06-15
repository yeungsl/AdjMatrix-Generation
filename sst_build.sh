#!/bin/bash
########################################################
# a script to build sst,
# plz run it inside the directory you want to build SST.
#
#### System requirement:
#         Linux Kernel below 4.0
#         gcc 3.4 or later
#         Ubuntu 14.04 preferred
########################################################


echo "Start building working SST 7.1.0 in "$PWD

echo "Fetching files needed"

wget -P $PWD https://www.open-mpi.org/software/ompi/v1.8/downloads/openmpi-1.8.8.tar.gz
wget -P $PWD http://software.intel.com/sites/landingpage/pintool/downloads/pin-2.14-71313-gcc.4.4.7-linux.tar.gz
wget -P $PWD https://github.com/sstsimulator/sst-core/releases/download/v7.1.0_Final/sstcore-7.1.0.tar.gz
wget -P $PWD https://github.com/sstsimulator/sst-elements/releases/download/v7.1.0_Final/sstelements-7.1.0.tar.gz

tar -xzvf openmpi-1.8.8.tar.gz
