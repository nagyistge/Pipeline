# -*- coding: utf-8 -*-
"""
BreastCAD pipeline utils.
@author: Maggie Kusano
@date: December 29, 2015
"""

import os
import SimpleITK as sitk
from pipeline_params_Lara import *


def build_tasklist():
    fileobj = open(TASK_FILE, "r")
    list = []
    try:
        for line in fileobj:
            # Get the study and accession number.
            lineparts = line.split()
            list.append([lineparts[0], lineparts[2]])
    finally:
        fileobj.close()

    list = sorted(list, key=lambda x: (int(x[0]), int(x[1])), reverse=True)

    tasklist = []
    task = []
    seen = set()
    fixed_assession = ""
    for line in list:
        study = line[0]
        assession = line[1]
        if study not in seen:
            seen.add(study)
            task.append(study)
            task.append(assession)
            fixed_assession = assession
        elif len(task) == 2:
            task.append(assession)
            tasklist.append(task)
            task = []
        else:
            task.append(study)
            task.append(fixed_assession)
            task.append(assession)
            tasklist.append(task)
            task = []

    for line in tasklist:
        print line[0], line[1], line[2]

    return tasklist


def build_tasklist_Lara(task_file=None):
    if not task_file:
        task_file = TASK_FILE
    fileobj = open(task_file, "r")
    list = []
    try:
        for line in fileobj:
            # Get the study and accession number.
            lineparts = line.split()
            list.append([lineparts[0], lineparts[2]])
    finally:
        fileobj.close()

    list = sorted(list, key=lambda x: (int(x[0]), int(x[1])), reverse=True)

    tasklist = []
    task = []
    seen = set()
    for line in list:
        patientId = line[0]
        accession = line[1]
        if patientId not in seen:
            if task:
                tasklist.append(task)
                task = []
            seen.add(patientId)
            task.append(patientId)
            task.append(accession)
        elif accession not in task:
            task.append(accession)
    if task:
        tasklist.append(task)

    return tasklist





