singularity \
    exec \
        --contain \
        --cleanenv \
        --pwd /Sample2 \
        --bind /mnt/seaes01-data01/dmg/dmg/mbcxpfh2/SpanishPlume/Analysis/Singularity/Sample/:/Sample2/ \
        ripdocker_latest.sif  \
        /bin/bash run.sh

# singularity \
#     shell \
#         --contain \
#         --cleanenv \
#         --pwd /Sample2 \
#         --bind /mnt/seaes01-data01/dmg/dmg/mbcxpfh2/SpanishPlume/Analysis/Singularity/Sample/:/Sample2/ \
#         ripdocker_latest.sif