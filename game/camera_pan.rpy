## Camera "reveal" pan over a whole scene (background + sprite move together,
## as if the character were standing still and the camera travels up them):
##   1. the character fades in at the normal framing,
##   2. the camera zooms down into the feet,
##   3. slowly pans up the body to the face,
##   4. zooms back out to the normal framing.
##
## How it works: camera_world() builds a "world" containing the background and
## the sprite placed exactly where they normally are, with a smooth dark floor
## continuing below the background (the sprite's feet are below the edge of the
## background, so there has to be something there). worldPan moves the camera.
##
## Needs gui/world_floor.png (made from the Mirror_Chamber background).
##
## NOTE: while the pan plays the scene is the world image, so expression
## changes (open/closed mouth) can't happen during it.

init python:

    def camera_world(bg, sprite, zoom, yoffset, floor="gui/world_floor.png",
                     xpos=960, height=1700):
        """
        bg      - path of the background, e.g. "bg/Mirror_Chamber.png"
        sprite  - image name of the sprite, e.g. "crhpycm"
        zoom    - the sprite's normal zoom (0.53 Crowley, 0.50 Adelaide)
        yoffset - the sprite's normal yoffset (380 Crowley, 450 Adelaide)
        floor   - image that continues the floor below the background (1920x620)
        xpos    - the sprite's normal horizontal centre, in pixels (960 = centre)
        height  - total height of the world, in pixels (1080 + floor height)
        """
        return Fixed(
            Transform(im.Scale(bg, 1920, 1080)),
            Transform(floor, ypos=1080),
            Transform(sprite, zoom=zoom, xanchor=0.5, xpos=xpos,
                      yanchor=1.0, ypos=1080 + yoffset),
            xysize=(1920, height))

    def cam_reveal_time(intro=0.7, dive=1.3, hold=0.5, pan=3.5, back=1.0):
        """Total running time of worldPan, in seconds."""
        return intro + dive + 2 * hold + pan + back


## One world per scene/character that gets a reveal. Add more as needed.
image crowley_world  = camera_world("bg/Mirror_Chamber.png", "crhpycm", 0.53, 380)
image adelaide_world = camera_world("bg/Mirror_Chamber.png", "adShockCm", 0.50, 450)


## cy0 = the point of the world the camera dives to first (down at the feet).
## cy1 = the point it ends on (up at the face).  Both are in world pixels,
##       measured from the top of the background.
##   Crowley :  worldPan(1194.0, 360.0)     (the defaults)
##   Adelaide:  worldPan(1232.0, 505.0)
transform worldPan(cy0=1194.0, cy1=360.0, zc=1.5,
                   intro=0.7,    # seconds at the normal framing (character fades in)
                   dive=1.3,     # seconds to zoom down into the feet
                   hold=0.5,     # pause on the feet, and again on the face
                   pan=3.5,      # seconds to travel from feet to face
                   back=1.0,     # seconds to zoom back out
                   height=1700.0):

    ## Start at the normal framing (looks identical to the regular scene).
    xanchor 0.5
    xpos 0.5
    ypos 0.5
    zoom 1.0
    yanchor (540.0 / height)
    pause intro

    ## Zoom down into the start of the pan.
    ease dive zoom zc yanchor (cy0 / height)
    pause hold

    ## Pan up the body.
    ease pan yanchor (cy1 / height)
    pause hold

    ## Zoom back out to the normal framing.
    easeout back zoom 1.0 yanchor (540.0 / height)
