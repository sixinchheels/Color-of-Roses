## Behind the in-game menu, show only the shaded background: no sprites.
##
## Ren'Py calls this label (if it exists) every time the game menu opens. It
## runs inside the menu's own copy of the scene, so the sprites are hidden
## there only. They are all back as soon as you return to the game.
##
## The background is the bottom-most image on the screen, i.e. the one shown
## with a "scene" statement; everything shown on top of it with "show" is hidden.

label enter_game_menu:

    python:
        if not main_menu:
            for _tag in renpy.get_showing_tags("master", sort=True)[1:]:
                renpy.hide(_tag, layer="master")

    return
