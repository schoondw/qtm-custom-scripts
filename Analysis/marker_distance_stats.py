'''Marker distance stats script
Script for analyzing the RMS distances of all marker pairs in a file.
It requires that all labeled markers have a rigid relationship with each other.
The RMS values are reported as averaged per trajectory and across all pairs.
The values give some more objective insight into the influence of artifacts/noise from the 3D tracker.
'''

# Make sure to import the QTM Scripting interface
import qtm

# Import libraries
import math
import numpy as np

# Set menu_priority to a positive integer if you want to use the startup_tools.py script
# to add the menu in this script to QTM
menu_priority = 0 

# Execution function: print "Hello world!" to the terminal
def _calc_dist_stats():
    # print("Hello world!") # Use QTM Scripting Interface method for writing to terminal
    traj_ids_all = qtm.data.object.trajectory.get_trajectory_ids()

    # Select labeled trajectories
    traj_ids = []
    for id in traj_ids_all:
        if not(qtm.data.object.trajectory.get_label(id) is None):
            traj_ids.append(id)
    n_trajs = len(traj_ids)
    # print("Number of labeled trajectories: {}".format(n_trajs))
    n_pairs = (n_trajs**2-n_trajs)/2

    # dist_stats = []
    RMS_av_traj = [0]*n_trajs # List of zeros of size n_trajs
    RMS_av_tot = 0
    # print("Marker pairs (RMS):")
    for i in range(n_trajs):
        lab1 = qtm.data.object.trajectory.get_label(traj_ids[i])
        for j in range(i+1,n_trajs):
            lab2 = qtm.data.object.trajectory.get_label(traj_ids[j])
            D = _calc_dist(traj_ids[i], traj_ids[j])
            RMS_av_traj[i] = RMS_av_traj[i] + np.std(D)/(n_trajs-1)
            RMS_av_traj[j] = RMS_av_traj[j] + np.std(D)/(n_trajs-1)
            RMS_av_tot = RMS_av_tot + np.std(D)/n_pairs
            # dist_stats.append({"pair": lab1 + "-" + lab2,"RMS": np.std(D)})
            # print("- {l1}-{l2}: {val}".format(l1=lab1, l2=lab2, val=np.std(D)))
    
    # Reporting
    print("\n--- Report for current file ---")
    print("RMS distance average TOT: {}".format(RMS_av_tot))

    print("RMS distance average per trajectory:")
    for i in range(n_trajs):
        lab = qtm.data.object.trajectory.get_label(traj_ids[i])
        print("- {lab}: {val}".format(lab=lab, val=RMS_av_traj[i]))


def _calc_dist(id1,id2):
    sr = qtm.gui.timeline.get_selected_range()
    D = np.array([])
    for frame in range(sr["start"],sr["end"]):
        s1 = qtm.data.series._3d.get_sample(id1, frame)
        s2 = qtm.data.series._3d.get_sample(id2, frame)
        if not(s1 is None or s2 is None):
            D = np.append(D, \
                        math.sqrt((s1["position"][0]-s2["position"][0])**2 + \
                        (s1["position"][1]-s2["position"][1])**2 + \
                        (s1["position"][2]-s2["position"][2])**2))
    return D


# Function for defining the commands and set up the menu
def add_menu():
    # Add command for display of script doc string to the terminal
    help_command = "disp_hello_world_script_doc" # Use a unique command name for display of script help
    qtm.gui.add_command(help_command)
    qtm.gui.set_command_execute_function(help_command, lambda:(print(__doc__)))

    # Add QTM command and set _echo_hello as execute function
    qtm.gui.add_command("calc_dist_stats")
    qtm.gui.set_command_execute_function("calc_dist_stats", _calc_dist_stats)

    # Add menu
    menu_id = qtm.gui.insert_menu_submenu(None, "Analyze")

    # Add Help button for display of the script doc string
    qtm.gui.insert_menu_button(menu_id, "Help", help_command)
    qtm.gui.insert_menu_separator(menu_id)

    # Add Hello world button
    qtm.gui.insert_menu_button(menu_id, "Marker distance stats", "calc_dist_stats")

# Call add_menu() function when running the script as stand-alone
if __name__ == "__main__":
    add_menu()
