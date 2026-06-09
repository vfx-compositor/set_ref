import nuke
import JM_set_ref

_menu = nuke.menu("Nuke").addMenu("JM Tools")
_menu.addCommand("Set Ref (CornerPin / Transform)", "JM_set_ref.set_ref()", "shift+c")
