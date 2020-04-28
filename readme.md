# SkeletoNet, Registration as Preprocessing

Jeremy Fisher, submission for MMiA 16-725

## Introduction

One of my personal projects this semester has been to submit an entry to the [RA2 Dream Challenge](https://www.synapse.org/#!Synapse:syn20545111/wiki/594083), a biomedical data science competition to automatically assess skeletal damage from rheumatoid arthritis in radiographs. The data provided include radiographs for several hundred patients in various stages of the disorder, as well as a Sharp/van der Heijde score. This is a metric, estimated manually by radiologists, to quantify deterioration and narrowing of the joints in the hands and feet. The goal of the competition is to derive the score from the radiograph.

Currently, I have trained two models per appendage: one to determine joint positions from the radiograph, another predict the score from just the relevant joint pixels. I have a fully functional pipeline, although it performs no better than a baseline model (i.e., one that predicts the mode of the distribution of  Sharp/van der Heijde score). In an original version of the dataset, a non-trivial number of radiographs were misaligned. For example, a radiograph of a left foot could be labeled as a right hand. Alternately, a radiograph could be rotated 45 degrees. In either case, I suspected that model performance could be improved by addressing these misalignments.

During the course of development, the organizers of the RA2 challenge updated the dataset such that fewer misalignments. There are still a few images that benefit from alignment: for instance, `UAB522-LH`.

## How to Compile and Run
My recommendation is to use Docker, as this should build regardless of operating system and python runtime. The command is simply:
```bash
make demonstration
```
This will build the docker image, set up a container with the correct bindings and run the algorithm on the RA2 dataset, depositing the results in a folder, `out`.

However, because this is a python package, it is simple to install in a conda enviornment:

```bash
conda create -n jeremy-mimia-final-project python=3.7
conda activate jeremy-mimia-final-project
pip install -r requirements.txt
python setup.py install
```
The minimum required python is version 3.6. This creates a command line program, `skeleregister`, that takes a file path to a radiograph and exports the registered and resampled image. For instance, the following should produce register radiographs in the RA2 dataset provided.

```bash
mkdir out && skeleregister --outdir ./out ./data
```

In either case, the program produced preprocessed and registered imaged as well as comparisons of those images to the original in the `out/registered` and `out/comparison` folders respectively.