"""
This program reads in data points which have associated individual errors.
Additionally, it reads a "step" size `x`.
Then it probes the data for points which follow the pattern: 
    y_1 = y_2 + x = y_3 + 2x
That is, it finds 3 data points which successively ascend by an interval `x`
up to the errors associated with the points.
"""

import tkinter as tk
from tkinter.filedialog import askopenfilename, asksaveasfilename

import pandas as pd
import numpy as np

def get_input_filename():
    """
    Brings up dialogue box in which you can select input Excel file.

    Returns
    -------
        input_filename : string
    """
   
    # hides the base window
    root = tk.Tk()
    root.withdraw()

    # open dialogue box prompting filename
    filename = askopenfilename()
    return filename



def get_output_filename():
    """
    Brings up dialogue box in which you can type output Excel filename.

    Returns
    -------
        output_filename : string
    """
   
    # hides the base window
    root = tk.Tk()
    root.withdraw()

    # open dialogue box prompting filename
    filename = asksaveasfilename(filetypes=(('Excel', '*.xlsx'),))
    return filename




def get_step_pairs(data, errors, step_size):
    """
    Finds pairs of numbers in `data` that are separated by `step_size` up
    to error given by `errors`.
    Returns list of tuple of indices corresponding to pairs.
    Note that the indices in each tuple are in order of increasing data value
    -- e.g. (i, j) implies data[i] < data[j]

    Parameters
    ----------
        data : array
            data, some of whose elements will be separated by step size
        errors : array
            errors corresponding to each point of data
        step_size : float
            interval between successive data in a step pair

    Returns
    -------
        step_pairs : list of tuples
            List of tuples whose contents are indices of step pairs in `data`
    """

    # compare all datum pairs, add ones with `step_size` to list
    step_pairs = []
    for i in range(len(data)):
        lower_bound = data[i] - errors[i]
        upper_bound = data[i] + errors[i]

        # only need to look from index i + 1 to end to get all pairs
        for j in range(i + 1, len(data)):

            diff_bound_1 = np.abs( lower_bound - (data[j] + errors[i]) )
            diff_bound_2 = np.abs( upper_bound - (data[j] - errors[i]) )
            diff_bound_max = max(diff_bound_1, diff_bound_2)
            diff_bound_min = min(diff_bound_1, diff_bound_2)

            if ( (step_size < diff_bound_max) and (step_size > diff_bound_min) ):
                lower_pair = i if data[i] < data[j] else j
                upper_pair = i if data[i] > data[j] else j
                step_pairs.append( (lower_pair, upper_pair) )

    return step_pairs
            


def get_step_triples(step_pairs):
    """
    Takes list of step pairs and creates list of step triples -- this is 
    dictated by step pairs sharing an index on opposite sides, e.g. 
    (123, 128) and (128, 114) would go to (123, 128, 114).

    Parameters
    ----------
    """
   
    step_triples = []
    for i in range(len(step_pairs)):
        for j in range(i + 1, len(step_pairs)):

            # if step_pairs match up on either end, write triple in ascending order
            if (step_pairs[i][1] == step_pairs[j][0]):
                step_triples.append( (step_pairs[i][0], 
                                      step_pairs[i][1], 
                                      step_pairs[j][1]) )

            elif (step_pairs[i][0] == step_pairs[j][1]):
                step_triples.append( (step_pairs[j][0], 
                                      step_pairs[i][0], 
                                      step_pairs[i][1]) )

    return step_triples
                


def main():

    input_filename = get_input_filename()
    data = pd.read_excel(input_filename)

    mz_data = data['m/z'].values
    errors = data['Error'].values
    step_size = data['delta m/z'][0]

    step_pairs = get_step_pairs(mz_data, errors, step_size)
    step_triples = get_step_triples(step_pairs)

    for step_triple in step_triples:
        print("Value: {}, Error: {}".format(mz_data[step_triple[0]], 
                                            errors[step_triple[0]]))
        print("Value: {}, Error: {}".format(mz_data[step_triple[1]], 
                                            errors[step_triple[1]]))
        print("Value: {}, Error: {}".format(mz_data[step_triple[2]], 
                                            errors[step_triple[2]]))
        print()

    step_triples_column = np.zeros(mz_data.shape, dtype=np.int64)
    for step_triple in step_triples:
        for idx in step_triple:
            step_triples_column[idx] = 1

    data['is homologue series'] = step_triples_column

    output_filename = get_output_filename()
    data.to_excel(output_filename)



if __name__ == "__main__":
    main()
