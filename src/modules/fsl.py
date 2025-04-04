#!/usr/bin/env python
# -*- coding : utf-8 -*-
"""
    FSL wrapper functions for DKIFA FSL calc functions. Add as needed.
"""

import subprocess

def statsmean(input_file,output_txtfile):

    """ Call FSL to run fslstats for Mean

    """
    arg = [
        "fslstats",
        input_file,
        "-M",
        " > ",
        output_txtfile,
    ]
    #completion = subprocess.run(arg)

    #if completion.returncode != 0:
    #    raise Exception(
    #        "Error in calculating mean of file: {}".format(input_file)
    #    )
    
    return arg

def createarg(input_file,output_file):

    """ Call FSL to run fslstats for Mean

    """
    arg = [
        "fslstats",
        input_file,
        "-M",
        " > ",
        output_file,
    ]

    return arg

def createarg2(input_file,output_file):

    """ Call FSL to run fslstats for Mean

    """
    arg = f'fslstats {input_file} -M > {output_file}'

    return arg