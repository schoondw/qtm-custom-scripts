'''modify_range.py: Modify selected measurement range.

Adds menu to QTM with following items:
* Modify selected range: crops current selected range at start and end as specified by crop_frames parameter.
  Use negative values for crop_frames to expand the selected range.
'''

# Create script file starting with `import qtm`
import qtm

# menu_priority = 1 # To be defined when loading with startup_tools.py

crop_frames = 50 # Use negative number to expand the selected range

# Function for modification of selected range
def _mod_range():
    mr = qtm.gui.timeline.get_measured_range()
    sr = qtm.gui.timeline.get_selected_range()
    sr['start']+=crop_frames
    sr['end']-=crop_frames
    if sr['start'] < mr['start']:
        sr['start'] = mr['start'] # set to start of measurement range
    if sr['end'] > mr['end']:
        sr['end'] = mr ['end'] # set to end of measurement range
    if sr['start'] >= sr['end']:
        qtm.gui.message.add_message("Warning::mod_range: Invalid selection range","Selected range too small: modification not applied.","warning")
        return # skip
    qtm.gui.timeline.set_selected_range(sr)
    qtm.gui.message.add_message("mod_range successfully applied",f"Selected range: {sr}.","info")

# Function for defining the commands and set up the menu
def add_menu():
    # Add QTM command
    qtm.gui.add_command("mod_range")
    qtm.gui.set_command_execute_function("mod_range", _mod_range)

    # Add menu and button
    menu_id = qtm.gui.insert_menu_submenu(None, "My menu")
    qtm.gui.insert_menu_button(menu_id, "Modify selected range", "mod_range")

# Call add_menu() function when running the script
if __name__ == "__main__":
    add_menu()
