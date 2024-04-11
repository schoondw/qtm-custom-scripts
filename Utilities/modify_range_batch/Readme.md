# Modify range batch

Scripts for automatic modification of the selected range of QTM files.

Pair of scripts:
* modify_range_script.py: QTM script, adding a custom command and menu to QTM.
* modify_range_batch.py: Python script using QTM RestAPI for batch processing according to predefined data folder structure.

The QTM script can be added to QTM. It will add a menu to QTM, allowing the user to modify the selected range by a button press.

The batch script can be used to batch process across all files in a QTM project. The data folder should be organized as follows:
* Subject (folder containing sessions)
    * Session (folder containing QTM files)

## Install

### Python

Install Python version 3.11 or higher from https://www.python.org/downloads/

* Make sure to add Python to the system path when installing.

Required packages (use pip install):

* requests

### QTM

Add the script *modify_range_script.py* to the QTM project.

Make sure that the parameter `crop_frame` is specified as desired (use negative value to expand the selected range).

## Instructions for use

**WARNING:**
* The batch script will modify all files in the project.
* If you have a large project, this may take a while.
* Make sure to keep a recent back up of the project before running the batch script.

Before running the batch script:
* Open a file in QTM and click the *Modify selected range* command from the custom menu in QTM to test that selected range is changed as expected.

Run the batch script:
* Open a terminal (e.g. windows cmd)
* Change directory to the folder containing *modify_range_batch.py*
* Locate the QTM project folder: `<qtm_proj_folder>`
* Type the command: `python modify_range_batch.py <qtm_proj_folder>`
