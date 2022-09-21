#/bin/bash

source /miniconda3/etc/profile.d/conda.sh && conda activate ncl_stable

ripdp_wrfarw RIPDP/rdp_sample all WRFData/wrfout_d01_*
rip -f RIPDP/rdp_sample rip_sample.in

cd BackTraj
rip -f ../RIPDP/rdp_sample traj1.in
rip -f ../RIPDP/rdp_sample traj2.in
rip -f ../RIPDP/rdp_sample traj3.in

rip -f ../RIPDP/rdp_sample traj_plot.in