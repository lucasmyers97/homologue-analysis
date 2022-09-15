# Homologue series analysis script

The purpose of this script is to use mass-spec data from polymers to determine whether each is in a homologue series.
That is, are the mass-spec data values part of a series where each consecutive value is separated from the last by some step.
To use, one specifies the data column, the error column, and a step on the command line, and then chooses an input file from a pop-up.
The program then writes a new file (filename determined by the user) which has the old data, and a separate column with a 1 or a 0 indicating whether that data point is part of a homologue series.

### Usage

To use on Windows, bring up the Anaconda command prompt by searching for "Anaconda" in the search bar.
Go to the appropriate directory where the script is:
```
cd path\to\my\script
```
Typically this will be under `C:\Users\[your-username]\homologue-analysis`.
To run the script, the syntax is:
```
python homologue_analysis.py [command-line-args]
```
The command-line arguments are `--data_dolumn`, `--error_column`, `--step_size`.
So, for example, to call the script one might type:
```
python homologue_analysis.py --data_column m/z --error_column Error --step_size 71.037114
```
One last note is that, when specifying the output filename, you must explicitly include the `.xlsx` file extension, otherwise the script will crash.

### Updating the script
If the script is ever updated, the update will be pushed to Github. 
To update your local copy, go to the directory where the script lives (see above), and then run:
```
git pull
```
So long as you have not made any changes to the script, it should run without intervention.
If you have made changes, it will likely prompt you to commit the changes you've made.
In that case, you'll have to commit those changes and then merge those with the upstream commits (outside the scope of this README).

### Contact info
Email: lucasmyers97@gmail.com
