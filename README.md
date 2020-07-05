# Navigation for the Node Editor in Blender
A Blender script that adds a gizmo to the top right of node editors that shows an overview of all of the nodes, and where the view is at.

It's like the minimap on a HUD in a game, or the navigator on an image editor.

![Screenshot of new minimap navigation](https://github.com/echowarp/blender_node_editor_navigation/raw/master/doc/img/NavigationPreviewShader.png "Screenshot of new minimap navigation")

# Installation: (Temporary)
1. Go to the scripting workspace
2. Add a "new text" at the top
3. Paste in "[gizmo_node_nav.py](https://github.com/echowarp/blender_node_editor_navigation/blob/master/gizmo_node_nav.py)" file contents into the text, or [download the file](https://raw.githubusercontent.com/echowarp/blender_node_editor_navigation/master/gizmo_node_nav.py) and select it with the file browser.
4. Hit "Run Script" at the top

![Screenshot showing the described installation steps](https://github.com/echowarp/blender_node_editor_navigation/raw/master/doc/img/InstallationSteps.png "Temporary Installation Steps")

Since this is not an addon, the navigator will only be shown until this blender instance is closed.
To use it again when reloading a save, just hit the run button.
For now, this is intentional until the stability of the script is better tested. If there is a crash or bug, this script will not be automatically loaded.

# Usage
Click and drag on the navigator to move the viewport.

# Known issues
* The main minimap gizmo disappears while dragging to navigate.

* Zooming and scrolling without the gizmo does not trigger a redraw.
Only changes in selection or moving using the minimap causes redraw.

# Feature ideas
* If possible, changing minimap node colors to match the colors at the top of the nodes in the view, and obey custom colors.

* Make minimap resizable by user.

* Once proven stable, convert to an addon for permanent installation.

* Obey user color scheme

# Motivation
I created this because I found the gizmo on the 3D view extremely helpful when using a graphics tablet, like a Wacom Intuos, but then found it extremely frustrating to navigate the node editor. The primary goal was just to add the scrolling by mouse drag that is possible in the 3D viewer.
