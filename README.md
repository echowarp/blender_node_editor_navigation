# Navigation for the Node Editor in Blender
A Blender script that adds a gizmo to the top right of node editors that shows an overview of all of the nodes, and where the view is at.

It's like the minimap on a HUD in a game, or the navigator on an image editor.


# Installation:
1. Go to the scripting workspace
2. Add a "new text" at the top
3. Paste in this file, or select this file in the browser if it was downloaded
4. Hit "Run Script" at the top

Since this is not an addon, the navigator will only be shown until this blender instance is closed.
To use it again when reloading a save, just hit the run button.
For now, this is intentional until the stability of the script is better tested.

# Usage
Click and drag on the navigator to move the viewport.

# Known issues
* The main minimap gizmo disappears while dragging to navigate.

* Zooming and scrolling without the gizmo does not trigger a redraw.
Only changes in selection or moving using the minimap causes redraw.
