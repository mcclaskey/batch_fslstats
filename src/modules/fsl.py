#!/usr/bin/env python
# -*- coding : utf-8 -*-

"""
    FSL wrapper functions for FSL functions. Add as needed.
"""

import subprocess

def fslstats_Mean(input_file):

    """ Call FSL to run fslstats for Mean and return output

    """
    fslcmd = [
        "fslstats",
        input_file,
        "-M",
    ]
    fsloutput = subprocess.run(fslcmd, capture_output=True, text=True)

    if fsloutput.returncode != 0:
        raise Exception(
            f"Error in calculating mean of file: {input_file}"
        )
    
    # return output as a float
    return float(fsloutput.stdout)
