## "Rose garland" navigation menu.
##
## The menu no longer lives in a sidebar. A rose vine drapes across the top of
## the screen and every menu entry hangs from it on a little tag:
##   - hover:    the bud on the vine blooms and the tag swings like a pendulum.
##   - current:  the page you are on hangs lower, with its bud in bloom, and
##               sways gently.
## The tags are rose-framed boxes (gui/menu_option_tag*.png), all the same size
## and all the same distance apart:
##   History, Save, Load, Preferences, Help, About, Main Menu, Quit.
##
## With the sidebar gone, the page content is re-centred and the old red
## divider is dropped (the overlay png that drew it is replaced by a plain
## 80% black, which is what the overlay was doing anyway).
##
## Setup: replace the old vine_menu.rpy with this file. In screens.rpy,
## "screen navigation():" must be renamed to "screen navigation_old():" (the
## same one-line edit as before). Tuned for the 1920x1080 PC menu.

define vine_red      = "#9b0000"
define vine_hot      = "#ff3355"
define vine_petal    = "#ffd9df"
define vine_rope     = "#7a0000"
define vine_leaf     = "#2f5d34"
define garland_fill  = "#2b0000"

## The rose boxes (gui/menu_option_tag.png, and gui/menu_option_tag_hover.png for
## the lit-up state). Both images are stored at 2x and shown at half size.
##   tag_w / tag_gap  - width of one box (roses included) and the EQUAL gap left
##                      between every pair of boxes
##   tag_text_size    - label size; the longest label ("Main Menu") leaves about
##                      14 px between its letters and the red rim on each side
define tag_w         = 172
define tag_gap       = 10
define tag_art_h     = 80       # height of the box art (roses included)
define tag_pad       = 8        # transparent margin round the art (room for the glow)
define tag_art_y     = 22       # where the art starts below the vine
define tag_string    = 36       # the string, from the vine down to the box's rim
define tag_inner_cx  = 86       # centre of the red opening, from the art's left edge
define tag_inner_cy  = 39       # centre of the red opening, from the art's top edge
define tag_text_size = 24

## Where the row of boxes is centred (the page title sits at the top-left of the
## game menu, so its row is centred a little to the right of the screen).
define tag_row_cx_game = 1165
define tag_row_cx_main = 960

## Roses that hang where each tag meets the vine (gui/shaded_menu_rose.png while
## idle, gui/menu_rose.png on hover), and the shade laid over the scene that
## shows behind the in-game menu (the last two digits are the opacity).
define rose_size     = 56
define menu_shade    = "#05000aa6"

init python:

    import math

    ## Where the tags and roses hang, measured from the lower edge of
    ## gui/vine.png (shown at half size, 1920x120): the height of that line at
    ## every 20 px across the screen, from x = 0 to x = 1920.
    ## (Positions handed to Ren'Py must be ints: a float means "fraction of the screen".)
    garland_line = [
        8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 11, 16,
        22, 26, 27, 28, 30, 34, 37, 41, 46, 49, 49, 49, 50,
        53, 55, 59, 63, 64, 63, 62, 64, 66, 67, 70, 72, 72,
        70, 68, 68, 68, 68, 69, 70, 68, 64, 62, 64, 68, 70,
        69, 68, 68, 68, 68, 70, 72, 72, 70, 67, 65, 64, 62,
        63, 64, 62, 59, 55, 52, 50, 48, 49, 49, 46, 41, 37,
        33, 30, 28, 27, 26, 22, 16, 11, 8, 8, 8, 8, 8,
        8, 8, 8, 8, 8, 8,
    ]

    def rope_y(x):
        i = max(0, min(int(x // 20), len(garland_line) - 2))
        f = (x - i * 20) / 20.0
        return garland_line[i] * (1.0 - f) + garland_line[i + 1] * f

    def vine_star(color, size=16):
        """Eight-point rosette made from two squares."""
        return Fixed(
            Transform(Solid(color, xysize=(size, size)), align=(0.5, 0.5)),
            Transform(Solid(color, xysize=(size, size)), rotate=45,
                      rotate_pad=False, align=(0.5, 0.5)),
            xysize=(40, 40))

## The garland itself: gui/vine.png is 3840x240, shown at half size.
define vine_garland_art = Transform("gui/vine.png", zoom=0.5)


## The bud on the vine: grows and spins when hovered, sways while current.
transform vine_bud(x, y):
    xpos x
    ypos y
    anchor (0.5, 0.5)
    transform_anchor True
    rotate_pad False
    zoom 1.0
    rotate 0
    on idle:
        easein 0.25 zoom 1.0 rotate 0
    on hover:
        easeout 0.30 zoom 1.9 rotate 90
    on selected_idle:
        easeout 0.30 zoom 1.9 rotate 90
        block:
            ease 1.4 rotate 80
            ease 1.4 rotate 100
            repeat
    on selected_hover:
        easeout 0.20 zoom 2.2 rotate 90

## Brighter red layer that fades in over the bud and the tag border.
transform vine_glow:
    alpha 0.0
    on idle:
        easein 0.25 alpha 0.0
    on hover:
        easeout 0.30 alpha 1.0
    on selected_idle:
        easeout 0.30 alpha 0.85
    on selected_hover:
        easeout 0.20 alpha 1.0

## Pale centre of the flower, opens on hover.
transform vine_core:
    align (0.5, 0.5)
    alpha 0.0
    on idle:
        easein 0.20 alpha 0.0
    on hover:
        easeout 0.30 alpha 1.0
    on selected_idle:
        easeout 0.30 alpha 1.0
    on selected_hover:
        easeout 0.20 alpha 1.0

## The rose on the vine: swells and turns a little when hovered, sways while current.
transform rose_bud(x, y):
    xpos x
    ypos y
    anchor (0.5, 0.5)
    transform_anchor True
    rotate_pad False
    zoom 1.0
    rotate 0
    on idle:
        easein 0.25 zoom 1.0 rotate 0
    on hover:
        easeout 0.30 zoom 1.22 rotate 18
    on selected_idle:
        easeout 0.30 zoom 1.22 rotate 0
        block:
            ease 1.4 rotate -8
            ease 1.4 rotate 8
            repeat
    on selected_hover:
        easeout 0.20 zoom 1.30 rotate 0

## The tag swings from the point where it hangs on the vine.
transform garland_swing(px):
    xpos px
    ypos 0
    anchor (px, 0)
    transform_anchor True
    rotate_pad False
    rotate 0
    yoffset 0
    on idle:
        easein 0.35 rotate 0 yoffset 0
    on hover:
        easeout 0.12 rotate -7 yoffset 10
        ease 0.28 rotate 5
        ease 0.30 rotate -3
        ease 0.30 rotate 1.5
        ease 0.30 rotate 0
    on selected_idle:
        easeout 0.25 yoffset 14
        block:
            ease 1.8 rotate 2.5
            ease 1.8 rotate -2.5
            repeat
    on selected_hover:
        easeout 0.12 rotate -5 yoffset 18
        ease 0.28 rotate 3
        ease 0.30 rotate 0


style garland_button is empty


## One hanging box.
##   x, y - where the box hangs from the vine (its horizontal centre)
screen garland_tag(label, act, x, y):

    $ px = tag_w // 2
    $ swing_h = tag_art_y + tag_art_h
    $ btn_h = swing_h + 26          ## spare room below, so the swing never leaves the hover area

    button:
        style "garland_button"
        xpos x - px
        ypos y
        xysize (tag_w, btn_h)
        action act

        fixed:
            xysize (tag_w, btn_h)

            ## The swinging part: string, rose box and label.
            fixed:
                xysize (tag_w, swing_h)
                at garland_swing(px)

                add Solid(vine_red, xysize=(2, tag_string)) xpos px - 1 ypos 0

                ## The rose box: the bright version fades in over it on hover.
                fixed:
                    pos (-tag_pad, tag_art_y - tag_pad)
                    xysize (tag_w + 2 * tag_pad, tag_art_h + 2 * tag_pad)

                    add Transform("gui/menu_option_tag.png", zoom=0.5)
                    add Transform("gui/menu_option_tag_hover.png", zoom=0.5) at vine_glow

                ## The label, centred in the red opening of the box.
                text label style "navigation_button_text":
                    size tag_text_size
                    anchor (0.5, 0.5)
                    pos (tag_inner_cx, tag_art_y + tag_inner_cy)

            ## The rose on the vine, where the box hangs: shaded while idle,
            ## the bright rose fades in on top of it when hovered.
            fixed:
                xysize (rose_size, rose_size)
                at rose_bud(px, 10)

                add "gui/shaded_menu_rose.png" zoom (rose_size / 512.0) align (0.5, 0.5)
                add "gui/menu_rose.png" zoom (rose_size / 512.0) align (0.5, 0.5) at vine_glow


screen navigation():

    add vine_garland_art

    python:
        entries = []

        if main_menu:
            entries.append((_("Start"), Start()))
        else:
            entries.append((_("History"), ShowMenu("history")))
            entries.append((_("Save"), ShowMenu("save")))
        entries.append((_("Load"), ShowMenu("load")))

        entries.append((_("Preferences"), ShowMenu("preferences")))
        if renpy.variant("pc") or (renpy.variant("web") and not renpy.variant("mobile")):
            entries.append((_("Help"), ShowMenu("help")))
        entries.append((_("About"), ShowMenu("about")))

        if _in_replay:
            entries.append((_("End Replay"), EndReplay(confirm=True)))
        elif not main_menu:
            entries.append((_("Main Menu"), MainMenu()))
        if renpy.variant("pc"):
            entries.append((_("Quit"), Quit(confirm=not main_menu)))

        ## One row, every box the same size and the same distance from the next.
        row_cx = tag_row_cx_main if main_menu else tag_row_cx_game
        count = len(entries)
        row_w = count * tag_w + (count - 1) * tag_gap
        row_l = int(round(row_cx - row_w / 2.0))

        placed = []
        for i, (lab, act) in enumerate(entries):
            placed.append((lab, act, row_l + tag_w // 2 + i * (tag_w + tag_gap)))

    for lab, act, tx in placed:
        use garland_tag(lab, act, tx, int(rope_y(tx)))


## The sidebar is gone, so give the page its width back and centre it.
style game_menu_navigation_frame:
    xsize 0

style game_menu_content_frame:
    left_margin 255
    right_margin 255

## The shading behind the page is drawn by screen game_menu itself (in
## screens.rpy), so the frame needs no background of its own.
style game_menu_outer_frame:
    background None

## The main menu's dark left strip is no longer needed either.
style main_menu_frame:
    background None
