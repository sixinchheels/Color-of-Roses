## Camera "reveal" pan: the background and the sprite zoom and travel together.
##   1. the black silhouette fades in at the normal framing,
##   2. the camera zooms in, ending at the bottom of the background,
##   3. the camera pans up the figure towards the face,
##   4. halfway through the pan the silhouette fades into the real sprite,
##   5. the camera holds on the face, then zooms back out to the normal framing.
##
## The camera never leaves the background: at zoom zc the view is
## 1920/zc by 1080/zc pixels, and the camera centre is clamped so that
## view stays inside the 1920x1080 background. No floor image is needed.
##
## NOTE: while the pan plays the scene is the "world" image, so expression
## changes (open/closed mouth) can't happen during it.

init python:

    ## Timings (seconds). The camera and the sprite layers both read these, so
    ## change them here and everything stays in sync.
    CAM_SIL_IN = 0.8    # silhouette fades in at the normal framing
    CAM_BEAT   = 0.5    # pause on the silhouette before the zoom starts
    CAM_DIVE   = 1.3    # zoom in to the bottom
    CAM_HOLD   = 0.5    # pause at the bottom before panning, and again on the face
    CAM_PAN    = 3.5    # travel from the bottom up to the face
    CAM_MORPH  = 1.0    # silhouette -> real sprite; centred on the middle of the pan

    def camera_world(bg, sprite, zoom, yoffset, xpos=960, sil=None, sil_zoom=None):
        """
        bg       - path of the background, e.g. "bg/Mirror_Chamber.png"
        sprite   - image name of the sprite, e.g. "crhpycm"
        zoom     - the sprite's normal zoom (0.53 Crowley, 0.50 Adelaide)
        yoffset  - the sprite's normal yoffset (380 Crowley, 450 Adelaide)
        xpos     - the sprite's normal horizontal centre, in pixels
        sil      - optional silhouette image name. It appears first and fades
                   into the sprite mid-pan. If None, the sprite itself simply
                   fades in at the start.
        sil_zoom - zoom for the silhouette if its file is a different size from
                   the sprite's (crw_sil.png is 2x, so Crowley uses zoom / 2).
        """
        def placed(img, z):
            return Transform(img, zoom=z, xanchor=0.5, xpos=xpos,
                             yanchor=1.0, ypos=1080 + yoffset)

        layers = [Transform(im.Scale(bg, 1920, 1080))]

        if sil is None:
            layers.append(At(placed(sprite, zoom), sprite_appear(CAM_SIL_IN)))
        else:
            if sil_zoom is None:
                sil_zoom = zoom
            t_pan   = CAM_SIL_IN + CAM_BEAT + CAM_DIVE + CAM_HOLD
            t_morph = t_pan + (CAM_PAN - CAM_MORPH) / 2.0
            layers.append(At(placed(sil, sil_zoom),
                             sil_cycle(CAM_SIL_IN, t_morph + CAM_MORPH / 2.0, CAM_MORPH / 2.0)))
            layers.append(At(placed(sprite, zoom), sprite_morph(t_morph, CAM_MORPH)))

        return Crop((0, 0, 1920, 1080), Fixed(*layers, xysize=(1920, 1080)))

    def cam_cx(cx, zc):
        """Camera centre x, kept so the view stays inside the background."""
        half = 960.0 / zc
        return max(half, min(1920.0 - half, cx))

    def cam_cy(cy, zc):
        """Camera centre y, kept so the view stays inside the background."""
        half = 540.0 / zc
        return max(half, min(1080.0 - half, cy))

    def cam_reveal_time(back=1.0):
        """Total running time of worldPan, in seconds."""
        return CAM_SIL_IN + CAM_BEAT + CAM_DIVE + 2 * CAM_HOLD + CAM_PAN + back


## Without a silhouette: the sprite fades in at the start.
transform sprite_appear(fade):
    alpha 0.0
    linear fade alpha 1.0

## The silhouette fades in, stays solid while the real sprite fades in over it,
## then fades out over the second half of the morph. Staying solid means the
## figure never turns see-through in the middle of the crossfade.
## fade_in = seconds to appear, out_at = time (from the start) it begins to
## fade out, fade_out = seconds to disappear.
transform sil_cycle(fade_in, out_at, fade_out):
    alpha 0.0
    linear fade_in alpha 1.0
    pause out_at - fade_in
    linear fade_out alpha 0.0

## The real sprite waits for the middle of the pan, then fades in over the silhouette.
transform sprite_morph(wait, morph):
    alpha 0.0
    pause wait
    linear morph alpha 1.0


image crw_sil = "ch/Crowley/crw_sil.png"

## One world per scene/character that gets a reveal. Add more as needed.
image crowley_world  = camera_world("bg/Mirror_Chamber.png", "crhpycm", 0.53, 380,
                                    sil="crw_sil", sil_zoom=0.265)
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
                   back=1.0):    # seconds to zoom back out at the end

    ## Start at the normal framing (looks identical to the regular scene).
    xpos 0.5
    ypos 0.5
    zoom 1.0
    xanchor 0.5
    yanchor 0.5

    ## The silhouette fades in, then a short beat.
    pause CAM_SIL_IN + CAM_BEAT

    ## Zoom in, ending at the bottom of the background.
    ease CAM_DIVE zoom zc xanchor (cam_cx(cx, zc) / 1920.0) yanchor (cam_cy(cy0, zc) / 1080.0)
    pause CAM_HOLD

    ## Pan up the figure to the face (the sprite fades in over the middle of this).
    ease CAM_PAN yanchor (cam_cy(cy1, zc) / 1080.0)
    pause CAM_HOLD

    ## Zoom back out to the normal framing.
    easeout back zoom 1.0 xanchor 0.5 yanchor 0.5
