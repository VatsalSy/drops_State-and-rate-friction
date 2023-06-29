# drops_State-and-rate-friction

This repository is forked from [https://github.com/cwlindeman/drops.git](https://github.com/cwlindeman/drops.git) which documents the data and codes used for [[2023-Chole and Sidney Nagel]_State-and-rate friction in contact-line dynamics.pdf](https://doi.org/10.1103/PhysRevE.107.065111). In the paper, the authors have proposed a new overdamped dynamical model of contact-line motion is used to capture theexperimentally observed behavior for water on the silanized glass, where the phenomenological drag coefficientand the assumed equilibrium contact angle are the only inputs. The model is based on an analogy to solid-solid friction which is both intuitive and relevant. In this repository, I have added one extra file: [ContactLineModels.ipynb](ContactLineModels.ipynb) to compare the model presented in this paper with other models in the literature. All these models seems to be in agreement with a wide range of parameters: although with different contact line mobilities. This similarity comes from the similar nature of the forcing term used in these models -- for details see the Jupyter notebook.

The original README.md is as follows.

# drops
Data from drop aspiration experiments and code needed to plot and analyze it

Each folder contains data from different experiments. 

For water on silanized glass and water on gold, files are tab delimited: first column is contact angle (in degrees) and second column in width (in mm). Several experiments are grouped together in each txt file; will see a sudden jump in drop width at the beginning of a new experiment (plotting code is set up to identify this). 

For toluene on silanized glass, files are comma delimited with the first row specifying what's what. Width is in pixels. Each experiment is in a separate txt file. 

Wait time experiments are at 10 frames per second; flow rate experiments are at 2, 5, 10, 20, and 50 fps for 0.4, 1.0, 2.0, 5.0, and 10.0 uL/s, respectively. (Note that the pump didn't keep up at the fastest flow rates; for example what's nominally 10 uL/s is closer to 8.0. The exact correction factor for a given experiment can be found using getFlowRate.py)

Order of experiments (water on silanized glass):
Wait time 0: 0, 2, 5, 1, 3 min
Wait time 1: 0, 1, 2, 3, 4, 5 min
Wait time 2: 5, 4, 3, 2, 1, 0 min
Flow rate 0 and 1: 0.4, 2.0, 10. uL/s
Flow rate 2: 10., 2.0, 0.4 uL/s

Order of experiments (water on gold):
Wait time 0 and 1: 0, 2, 5, 10 min
Wait time reverse: 10, 5, 2, 0 min
Flow rate: 0.4, 1.0, 2.0, 5.0, 10. uL/s
Flow rate reverse: 10., 5.0, 2.0, 1.0, 0.4 uL/s

Data of a certain type can be plotted using the corresponding plot...Data.py. Just set exptType and the set number accordingly at the beginning of the python file. 

Overdamped model numerical integration happens in simulateData.py (uncomment "example" at the bottom and run to see resulting "data" for one set of parameters). Using actual water on silanized glass data to find best-fit equilibrium contact angle and damping coefficient parameters can be done using automatedDropFit.py but requires playing around with the code to set the range of parameters to try and what experimental datasets to fit.
