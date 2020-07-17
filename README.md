# Navigation for the Node Editor in Blender
A Blender script that adds a gizmo to the top right of node editors that shows an overview of all of the nodes, and where the view is at.

It's like the minimap on a HUD in a game, or the navigator on an image editor.

![Screenshot of new minimap navigation](https://github.com/echowarp/blender_node_editor_navigation/raw/master/doc/img/NavigationPreviewShader.png "Screenshot of new minimap navigation")

The minimap works in the shader editor and the compositor views.

# Installation as Add-on
This script is now available as an add-on.

1. [Download the add-on](https://raw.githubusercontent.com/echowarp/blender_node_editor_navigation/master/gizmo_node_nav.py).
2. Edit > Preferences > Addons > Install
3. Select your downloaded file
4. Enable the add-on with the checkmark
5. Optionally, in the bottom left, save preferences.

![Screenshot of installation as addon steps](https://github.com/echowarp/blender_node_editor_navigation/raw/master/doc/img/InstallationAddon.png "Screenshot of installation as addon steps")

# Installation: (Temporary)
You can try this as a temporary measure if you want to review the code and ensure nothing auto-runs if Blender crashes.

1. Go to the scripting workspace
2. Add a "new text" at the top
3. Paste in "[gizmo_node_nav.py](https://github.com/echowarp/blender_node_editor_navigation/blob/master/gizmo_node_nav.py)" file contents into the text, or [download the file](https://raw.githubusercontent.com/echowarp/blender_node_editor_navigation/master/gizmo_node_nav.py) and select it with the file browser.
4. Hit "Run Script" at the top

![Screenshot showing the described script execution steps](https://github.com/echowarp/blender_node_editor_navigation/raw/master/doc/img/InstallationSteps.png "Temporary Installation Steps")

Since this is not an addon, the navigator will only be shown until this blender instance is closed.
To use it again when reloading a save, just hit the run button.

# Usage
Click and drag on the navigator to move the viewport.

# Known issues
* The main background gizmo disappears while dragging to navigate.

* Zooming and scrolling without the gizmo does not trigger a redraw.
Only changes in selection or moving using the minimap causes redraw.

# Feature ideas
* If possible, changing minimap node colors to match the colors at the top of the nodes in the view, and highlight nodes with custom colors.

* Make minimap resizable by user in user configuration.

* Obey user color scheme

# Motivation
I created this because I found the gizmo on the 3D view extremely helpful when using a graphics tablet, like a Wacom Intuos, but then found it extremely frustrating to navigate the node editor. The primary goal was just to add the scrolling by mouse drag that is possible in the 3D viewer.
