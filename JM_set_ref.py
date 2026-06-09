# JM_cornerpin_set_ref.py
import nuke
import re


# --------- Shared ---------
def _update_label(node, frame):
    """Replace existing 'ref: N' line, prepend it, or set it from empty."""
    label_knob = node['label']
    label_knob.clearAnimated()
    current = label_knob.value()
    ref_line = "ref: {}".format(frame)

    if re.search(r'^ref:\s*\d+', current, flags=re.MULTILINE):
        new_label = re.sub(r'^ref:\s*\d+.*$', ref_line, current, flags=re.MULTILINE)
    elif current.strip():
        new_label = ref_line + "\n" + current
    else:
        new_label = ref_line

    label_knob.setValue(new_label)


# --------- CornerPin2D ---------
def _set_ref_cornerpin(node, frame):
    """Bake current 'to' values into 'from' at the given frame."""
    for to_name, from_name in zip(
        ['to1', 'to2', 'to3', 'to4'],
        ['from1', 'from2', 'from3', 'from4']
    ):
        x, y = node[to_name].getValueAt(frame)
        from_knob = node[from_name]
        from_knob.clearAnimated()
        from_knob.setValue(x, 0)
        from_knob.setValue(y, 1)

    _update_label(node, frame)


# --------- Transform ---------
def _set_ref_transform(node, frame):
    """
    Normalize Transform animation so the current frame becomes the neutral pose.
    Adjusts keyframe values in-place — no extra nodes inserted.

    Note: exact only when 'center' is static. Animated center requires
    matrix composition (use an inverted upstream Transform instead).
    """
    # (knob_name, dims, operation)
    targets = [
        ('translate', 2, 'sub'),
        ('rotate',    1, 'sub'),
        ('scale',     2, 'div'),
        ('skew',      2, 'sub'),
    ]

    for name, dims, op in targets:
        knob = node[name]
        for ch in range(dims):
            ref_val = knob.getValueAt(frame, ch)

            if knob.isAnimated(ch):
                # Shift every key in this channel
                for key in knob.animation(ch).keys():
                    if op == 'sub':
                        key.y -= ref_val
                    elif op == 'div' and ref_val != 0:
                        key.y /= ref_val
            else:
                # Static channel: adjust the single value
                old = knob.getValue(ch)
                if op == 'sub':
                    knob.setValue(old - ref_val, ch)
                elif op == 'div' and ref_val != 0:
                    knob.setValue(old / ref_val, ch)

    _update_label(node, frame)


# --------- Main ---------
def set_ref():
    """Set reference pose on selected CornerPin2D / Transform nodes at the current frame."""
    nodes = [n for n in nuke.selectedNodes() if n.Class() in ('CornerPin2D', 'Transform')]

    if not nodes:
        nuke.message("Select at least one CornerPin2D or Transform node.")
        return

    try:
        frame = int(nuke.frame())
    except ValueError:
        return

    with nuke.Undo():
        for node in nodes:
            if node.Class() == 'CornerPin2D':
                _set_ref_cornerpin(node, frame)
            elif node.Class() == 'Transform':
                _set_ref_transform(node, frame)
