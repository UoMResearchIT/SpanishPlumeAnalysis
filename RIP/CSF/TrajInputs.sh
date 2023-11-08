#!/bin/bash

if [ "$1" = "" ]; then
    echo "You have to provide a name!"
    exit 1
fi

rip_dir="/mnt/seaes01-data01/dmg/dmg/mbcxpfh2/SpanishPlume/Analysis/RIP/"

echo "" > $1.inputs

for dataset in Control Double_hgt G_Wave_fix Half_hgt Zero_hgt; do
echo "-od="$rip_dir"ResultsCSF/"$dataset" -pd="$rip_dir"Results/RIPDP/"$dataset"/rdp_"$dataset" -tt=122 -tp="$dataset"_070402" >> $1.inputs
done
echo "" >> $1.inputs
for dataset in Control Double_hgt G_Wave_fix Half_hgt Zero_hgt; do
    echo "-od="$rip_dir"ResultsCSF/"$dataset" -pd="$rip_dir"Results/RIPDP/"$dataset"/rdp_"$dataset" -tt=120 -tp="$dataset"_070400" >> $1.inputs
    echo "-od="$rip_dir"ResultsCSF/"$dataset" -pd="$rip_dir"Results/RIPDP/"$dataset"/rdp_"$dataset" -tt=121 -tp="$dataset"_070401" >> $1.inputs
    echo "-od="$rip_dir"ResultsCSF/"$dataset" -pd="$rip_dir"Results/RIPDP/"$dataset"/rdp_"$dataset" -tt=123 -tp="$dataset"_070403" >> $1.inputs
    echo "-od="$rip_dir"ResultsCSF/"$dataset" -pd="$rip_dir"Results/RIPDP/"$dataset"/rdp_"$dataset" -tt=124 -tp="$dataset"_070404" >> $1.inputs
    echo "" >> $1.inputs
    echo "-od="$rip_dir"ResultsCSF/"$dataset" -pd="$rip_dir"Results/RIPDP/"$dataset"/rdp_"$dataset" -tt=66 -tp="$dataset"_070118" >> $1.inputs
    echo "-od="$rip_dir"ResultsCSF/"$dataset" -pd="$rip_dir"Results/RIPDP/"$dataset"/rdp_"$dataset" -tt=67 -tp="$dataset"_070119" >> $1.inputs
    echo "-od="$rip_dir"ResultsCSF/"$dataset" -pd="$rip_dir"Results/RIPDP/"$dataset"/rdp_"$dataset" -tt=68 -tp="$dataset"_070120" >> $1.inputs
    echo "-od="$rip_dir"ResultsCSF/"$dataset" -pd="$rip_dir"Results/RIPDP/"$dataset"/rdp_"$dataset" -tt=69 -tp="$dataset"_070121" >> $1.inputs
    echo "-od="$rip_dir"ResultsCSF/"$dataset" -pd="$rip_dir"Results/RIPDP/"$dataset"/rdp_"$dataset" -tt=70 -tp="$dataset"_070122" >> $1.inputs
    echo "" >> $1.inputs
done
echo "" >> $1.inputs