## Keeps the character's name visible while sprites change/transition.
## Ren'Py's default empty window used the narrator (no name); this uses the
## actual speaker instead.

init python:

    def empty_window_keep_name():
        who = None
        multiple = None

        try:
            scry = renpy.scry()
            window_hide = renpy.get_statement_name() == "window hide"

            if (scry.say or scry.menu_with_caption or store._window_next) and not window_hide:
                for i in range(20):
                    if scry.say:
                        who = scry.who
                        multiple = scry.multiple
                        break
                    scry = scry.next()
                    if scry is None:
                        break
            else:
                who = renpy.eval_who(store._last_say_who)
        except Exception:
            pass

        if who is None:
            who = store.narrator

        if isinstance(who, NVLCharacter):
            nvl_show_core()
        else:
            who.empty_window(multiple=multiple)

    config.empty_window = empty_window_keep_name


## Makes {i} and {b} text use the real Crimson Text italic/bold files
## instead of Ren'Py's faked versions.
init python:
    _ct = "font/CrimsonText-"
    config.font_replacement_map[_ct + "Regular.ttf", False, True] = (_ct + "Italic.ttf", False, False)
    config.font_replacement_map[_ct + "Regular.ttf", True, False] = (_ct + "Bold.ttf", False, False)
    config.font_replacement_map[_ct + "Regular.ttf", True, True] = (_ct + "BoldItalic.ttf", False, False)
