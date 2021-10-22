#!/bin/bash

awk -F, '{$2=$2+1}1' OFS=, usage.txt >tmp & mv tmp usage.txt
