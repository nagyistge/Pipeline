# -*- coding: utf-8 -*-
"""
Runs the optical flow motion correction step of the BreastCAD pipeline.
@author: Maggie Kusano
@date: November 26, 2015
"""

import os
import fnmatch

import pipeline_utils as utils
from BreastCAD import motion_correction
from pipeline_params_Lara import *


def main():
    """ Runs the Breast CAD pipeline
    """

    # ======================================================================================================================
    # Make sure everything exists before starting pipeline
    #
    if not os.path.isfile(TASK_FILE):
        print "ERROR: TASK_FILE (" + TASK_FILE + ") does not exist."
        return 1
    if not os.path.exists(OUTPUT_DIRECTORY):
        os.makedirs(OUTPUT_DIRECTORY)
    if not os.path.isfile(MOTIONCORRECTION_EXE):
        print "ERROR: invalid path to motion correction executable (" + MOTIONCORRECTION_EXE + ")."
        return 1

    # ==================================================================================================================
    # And go...
    #
    # Open study list.
    print "Generating task list..."
    tasklist = utils.build_tasklist_Lara()

    for iItem, item in enumerate(tasklist):

        _study_no = item[0]
        _accession_nos = item[1:]
        # Sort accession numbers so pre-biopsy scan is first.
        _accession_nos = sorted(_accession_nos, key=lambda x: int(x), reverse=True)

        # Make sure input data exists.
        _outputDir = OUTPUT_DIRECTORY + os.sep + _study_no
        if not os.path.exists(_outputDir):
            print "Study not found (" + _outputDir + "). Skipping."
            continue

        print "Processing Study: " + _study_no + "..."

        # --------------------------------------------------------------------------------------------------------------
        #  Perform optical flow motion correction on post-contrast images (align post-contrast to pre-contrast fat
        #  suppressed image).
        #
        print "    Motion correcting post-contrast images..."
        # Find pre and contrast-enhanced input files and mask file.
        contents = os.listdir(_outputDir)
        for accession_no in _accession_nos:
            matches = fnmatch.filter(contents, _study_no+"*"+accession_no+"*"+MOTIONCORRECTION_FIXED_IMG_TYPE_FILTER)
            fixed_file = os.path.join(_outputDir, matches[0])
            matches = fnmatch.filter(contents, _study_no+"*"+accession_no+"*"+MOTIONCORRECTION_MOVING_IMG_TYPE_FILTER)
            moving_files = []
            for match in matches:
                moving_files.append(os.path.join(_outputDir, match))

            motion_correction.do_motion_correction(MOTIONCORRECTION_EXE, fixed_file, moving_files)


if __name__ == '__main__':
    main()

