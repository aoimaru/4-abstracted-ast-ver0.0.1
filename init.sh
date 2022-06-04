#!/bin/sh

DICS=(
    "${PWD}/original-datasets"
    "${PWD}/self-made-metadata/created"
    "${PWD}/self-made-metadata/original"
    "${PWD}/self-made-model/github"
    "${PWD}/self-made-model/gold"
    "${PWD}/self-made-pickle/github"
    "${PWD}/self-made-pickle/gold"
    "${PWD}/self-made-datasets/github"
    "${PWD}/self-made-datasets/gold"
    "${PWD}/self-made-datasets/origin"
    "${PWD}/sample"
)


for DIC in "${DICS[@]}"; do
  [ ! -d "${DIC}" ] && mkdir -p ${DIC}
done