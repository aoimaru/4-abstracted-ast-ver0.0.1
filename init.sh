#!/bin/sh

DICS=(
    "./original-datasets"
    "./self-made-metadata/created"
    "./self-made-metadata/original"
    "./self-made-model/github"
    "./self-made-model/gold"
    "./self-made-pickle/github"
    "./self-made-pickle/gold"
    "./self-made-datasets/github"
    "./self-made-datasets/gold"
    "./self-made-datasets/origin"
)


for DIC in "${DICS[@]}"; do
  [ ! -d "${DIC}" ] && mkdir -p ${DIC}
done