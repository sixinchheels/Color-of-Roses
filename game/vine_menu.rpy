## "Rose garland" navigation menu.
##
## The menu no longer lives in a sidebar. A rose vine drapes across the top of
## the screen and every menu entry hangs from it on a little tag:
##   - hover:    the bud on the vine blooms and the tag swings like a pendulum.
##   - current:  the page you are on hangs lower, with its bud in bloom, and
##               sways gently.
## Entries are grouped, with a wider gap between groups:
##   Story (History, Save, Load) / Settings (Preferences, Help, About) /
##   Leave (Main Menu, Quit).
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
define garland_gap   = 26       # extra space between menu groups

init python:

    import math

    ## Height of the vine at horizontal position x: it sags in the middle.
    ## (Positions handed to Ren'Py must be ints: a float means "fraction of the screen".)
    def rope_y(x):
        return 6.0 + 40.0 * (1.0 - ((x - 960.0) / 960.0) ** 2)

    def vine_star(color, size=16):
        """Eight-point rosette made from two squares."""
        return Fixed(
            Transform(Solid(color, xysize=(size, size)), align=(0.5, 0.5)),
            Transform(Solid(color, xysize=(size, size)), rotate=45,
                      rotate_pad=False, align=(0.5, 0.5)),
            xysize=(40, 40))

    def vine_garland_art():
        """The vine itself: short rotated segments along rope_y, plus leaves."""
        parts = []
        step = 20

        for x0 in range(0, 1920, step):
            x1 = x0 + step
            y0, y1 = rope_y(x0), rope_y(x1)
            angle = math.degrees(math.atan2(y1 - y0, x1 - x0))
            parts.append(Transform(
                Solid(vine_rope, xysize=(step + 3, 5)),
                rotate=angle, rotate_pad=False,
                anchor=(0.5, 0.5),
                pos=(int(round((x0 + x1) / 2.0)), int(round((y0 + y1) / 2.0)))))

        side = 1
        for x in range(45, 1920, 95):
            y = rope_y(x)
            angle = math.degrees(math.atan2(rope_y(x + 1) - rope_y(x - 1), 2.0))
            leaf_angle = angle + side * 50
            rad = math.radians(leaf_angle)
            parts.append(Transform(
                Solid(vine_leaf, xysize=(18, 7)),
                rotate=leaf_angle, rotate_pad=False,
                anchor=(0.5, 0.5),
                pos=(int(round(x + 9 * math.cos(rad))), int(round(y + 9 * math.sin(rad))))))
            side = -side

        return Fixed(*parts, xysize=(1920, 120))

define vine_garland_art = vine_garland_art()


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


## One hanging tag.
##   x, y - where the tag hangs from the vine (its horizontal centre)
##   tw   - tag width
screen garland_tag(label, act, x, y, tw):

    $ th = 60
    $ px = tw // 2

    button:
        style "garland_button"
        xpos x - px
        ypos y
        xsize tw
        ysize 20 + th + 26      ## spare room below, so the swing never leaves the hover area
        action act

        fixed:
            xsize tw
            ysize 20 + th + 26

            ## The swinging part: string and tag.
            fixed:
                xysize (tw, 20 + th)
                at garland_swing(px)

                add Solid(vine_red, xysize=(2, 22)) xpos px - 1 ypos 0

                fixed:
                    xpos 0
                    ypos 20
                    xysize (tw, th)

                    add Solid(vine_red, xysize=(tw, th))
                    add Solid(vine_hot, xysize=(tw, th)) at vine_glow
                    add Solid(garland_fill, xysize=(tw - 4, th - 4)) pos (2, 2)

                    text label style "navigation_button_text" size 28 align (0.5, 0.5)

            ## The bud on the vine, where the tag hangs.
            fixed:
                xysize (40, 40)
                at vine_bud(px, 0)

                add vine_star(vine_red)
                add vine_star(vine_hot) at vine_glow
                add Solid(vine_petal, xysize=(6, 6)) at vine_core


screen navigation():

    add vine_garland_art

    python:
        groups = []

        story = []
        if main_menu:
            story.append((_("Start"), Start()))
        else:
            story.append((_("History"), ShowMenu("history")))
            story.append((_("Save"), ShowMenu("save")))
        story.append((_("Load"), ShowMenu("load")))
        groups.append(story)

        settings = [(_("Preferences"), ShowMenu("preferences"))]
        if renpy.variant("pc") or (renpy.variant("web") and not renpy.variant("mobile")):
            settings.append((_("Help"), ShowMenu("help")))
        settings.append((_("About"), ShowMenu("about")))
        groups.append(settings)

        leave = []
        if _in_replay:
            leave.append((_("End Replay"), EndReplay(confirm=True)))
        elif not main_menu:
            leave.append((_("Main Menu"), MainMenu()))
        if renpy.variant("pc"):
            leave.append((_("Quit"), Quit(confirm=not main_menu)))
        if leave:
            groups.append(leave)

        ## Spread the tags over the free part of the top edge (the page title
        ## sits at the top-left of the game menu; the main menu has no title there).
        if main_menu:
            region_l, region_r = 360, 1560
        else:
            region_l, region_r = 500, 1880

        count = sum(len(g) for g in groups)
        extra = garland_gap * (len(groups) - 1)
        slot = (region_r - region_l - extra) / float(count)
        tag_w = int(min(172, slot - 10))

        placed = []
        cx = region_l + slot / 2.0
        for gi, g in enumerate(groups):
            if gi:
                cx += garland_gap
            for lab, act in g:
                placed.append((lab, act, int(cx)))
                cx += slot

    for lab, act, tx in placed:
        use garland_tag(lab, act, tx, int(rope_y(tx)), tag_w)


## The sidebar is gone, so give the page its width back and centre it.
style game_menu_navigation_frame:
    xsize 0

style game_menu_content_frame:
    left_margin 255
    right_margin 255

## Same 80% black the old overlay png drew, minus its red divider line.
style game_menu_outer_frame:
    background Solid("#000000cc")

## The main menu's dark left strip is no longer needed either.
style main_menu_frame:
    background None
