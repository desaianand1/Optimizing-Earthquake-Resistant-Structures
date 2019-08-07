# Optimizing Earthquake-Resistant Structures

**This program aims to evolve stable, earthquake resistant towers using a simulated shake-table test.**

An evolutionary strategy approach is implemented with standard gaussian random variables used to mutate offspring,
following which elitist sorting is used to select the most fit individuals from the population.

The final, most stable structure was shown to be stable in multiple axes of shaking and could withstand varying
intensities of earthquakes. This solution had a fitness of **4886.76** and could be reasonably replicated for use in the
real world.

# Sample Structure
<img src="/solution%20results/best.PNG" width="400" height="400">

# Installation

**Requirements:**
* Install Python 3.2+ (**Recommended:** [Python 3.7.3](https://www.python.org/downloads/))
* Install [Anaconda 3.7](https://www.anaconda.com/distribution/)

**Install PyChrono library:**
</br>This project utilizes the PyChrono Engine for rigid-body physics simulation.
</br>Use the following command in the **Anaconda Command Prompt** to install PyChrono:
</br>`conda install -c projectchrono pychrono`

**Setting up the environment:**
</br>Open this project in an IDE of your choice. (**Recommended:** [PyCharm Community v2019.2](https://www.jetbrains.com/pycharm/download/#section=windows))
</br>Ensure that the project interpreter is set to the **Anaconda Interpreter**. This is usually located here:
* Windows: `C:\Users\%USER_NAME%\Anaconda3\python.exe`
* Linux: `/home/%USER_NAME%/anaconda/bin/python`
* OSX: `/Users/%USER_NAME%/anaconda/bin/python`

**Changing DATAPATH variable:**
</br>In [settings.py](/settings.py), change the `DATAPATH` variable to point to the ‘data’ folder in your **Anaconda** installation directory:
* For Windows: `C:\ProgramData\Anaconda3\Library\data\`

# Running Trials

1.	To run a new experiment, edit any parameters in [settings.py](/settings.py)
    *	Change the `EXP_NAME` variable in some way to prevent overwriting previously written csv files or plots when running a trial. All CSV files and plots generated for this experiment will follow this naming convention. 
    *	Changing the `EXP_NAME` variable will affect which plots and candidates are visualized when running [visualize_solutions.py](/utility/visualize_solutions.py) or [plot.py](/utility/plot.py)
    *	Run [main.py](main.py) to run the experiment.
2.	CSV files are generated when the new trial ends. Cancelling a running trial prematurely will not save any information to the CSV file.
    *	CSV files are saved in the `/data/` folder
    *	Plots are saved as PNG images in the `/plot/` folder
3.	To see the best candidate for a trial, run [visualize_solutions.py](/utility/visualize_solutions.py)
    *	If several trials were run, you may have to edit the `trial` variable to whatever trial’s candidate you want to visualize.
4.	To generate the plot for a trial, run [plot.py](/utility/plot.py)
    *	If several trials were run, you may have to edit the `trial` variable to whatever trial’s plot you want to generate.


