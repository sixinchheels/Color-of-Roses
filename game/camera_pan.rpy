## Camera "reveal" pan: the background and the sprite zoom and travel together.
##   1. a short beat on the empty background (no sprite yet),
##   2. the camera zooms in, ending at the bottom of the background,
##   3. the sprite fades in, the camera holding at the bottom,
##   4. the camera pans up the sprite to the face,
##   5. it zooms back out to the normal framing.
##
## The camera never leaves the background: at zoom zc the view is
## 1920/zc by 1080/zc pixels, and the camera centre is clamped so that
## view stays inside the 1920x1080 background. No floor image is needed.
##
## NOTE: while the pan plays the scene is the "world" image, so expression
## changes (open/closed mouth) can't happen during it.

init python:

    ## Timings shared by the camera and the sprite fade (seconds).
    CAM_INTRO  = 0.5    # empty background at the normal framing
    CAM_DIVE   = 1.3    # zoom in to the bottom
    CAM_APPEAR = 0.8    # sprite fades in while the camera holds at the bottom

    def camera_world(bg, sprite, zoom, yoffset, xpos=960):
        """
        bg      - path of the background, e.g. "bg/Mirror_Chamber.png"
        sprite  - image name of the sprite, e.g. "crhpycm"
        zoom    - the sprite's normal zoom (0.53 Crowley, 0.50 Adelaide)
        yoffset - the sprite's normal yoffset (380 Crowley, 450 Adelaide)
        xpos    - the sprite's normal horizontal centre, in pixels
        """
        placed = Transform(sprite, zoom=zoom, xanchor=0.5, xpos=xpos,
                           yanchor=1.0, ypos=1080 + yoffset)
        return Crop((0, 0, 1920, 1080), Fixed(
            Transform(im.Scale(bg, 1920, 1080)),
            At(placed, sprite_appear(CAM_INTRO + CAM_DIVE, CAM_APPEAR)),
            xysize=(1920, 1080)))

    def cam_cx(cx, zc):
        """Camera centre x, kept so the view stays inside the background."""
        half = 960.0 / zc
        return max(half, min(1920.0 - half, cx))

    def cam_cy(cy, zc):
        """Camera centre y, kept so the view stays inside the background."""
        half = 540.0 / zc
        return max(half, min(1080.0 - half, cy))

    def cam_reveal_time(hold=0.5, pan=3.5, back=1.0):
        """Total running time of worldPan, in seconds."""
        return CAM_INTRO + CAM_DIVE + CAM_APPEAR + 2 * hold + pan + back


## The sprite is invisible until the zoom has finished, then fades in.
transform sprite_appear(wait, fade):
    alpha 0.0
    pause wait
    linear fade alpha 1.0


## One world per scene/character that gets a reveal. Add more as needed.
image crowley_world  = camera_world("bg/Mirror_Chamber.png", "crhpycm", 0.53, 380)
image adelaide_world = camera_world("bg/Mirror_Chamber.png", "adShockCm", 0.50, 450)


## cx  = x of the world the camera stays on (960 = centre; clamped to the bg).
## cy0 = where the camera dives to first. The default (1080) means "as low as
##       possible": it gets clamped to the bottom edge of the background.
## cy1 = where it ends up, at the face, measured in world pixels from the top
##       of the background. It can't go above 540/zc (360 at the default zc),
##       so for a face higher than that, lower zc.
##   Crowley :  show crowley_world at worldPan
##   Adelaide:  show adelaide_world at worldPan(cy1=505.0)
transform worldPan(cx=960.0, cy0=1080.0, cy1=360.0, zc=1.5,
                   hold=0.5,     # pause after the sprite has appeared, and again on the face
                   pan=3.5,      # seconds to travel from bottom to face
                   back=1.0):    # seconds to zoom back out

    ## Start at the normal framing (looks identical to the regular scene).
    xpos 0.5
    ypos 0.5
    zoom 1.0
    xanchor 0.5
    yanchor 0.5
    pause CAM_INTRO

    ## Zoom in, ending at the bottom of the background.
    ease CAM_DIVE zoom zc xanchor (cam_cx(cx, zc) / 1920.0) yanchor (cam_cy(cy0, zc) / 1080.0)

    ## Hold while the sprite fades in, then a short pause.
    pause CAM_APPEAR
    pause hold

    ## Pan up the body to the face.
    ease pan yanchor (cam_cy(cy1, zc) / 1080.0)
    pause hold

    ## Zoom back out to the normal framing.
    easeout back zoom 1.0 xanchor 0.5 yanchor 0.5
