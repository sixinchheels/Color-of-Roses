## Book page-turn transition for the game menu (Esc).
##
## - Opening the menu: the game peels away like a page being turned from right
##   to left, revealing the menu underneath.
## - Leaving the menu: the page turns back over, from left to right.
##
## This uses a small custom shader (a cylinder "page curl"), so it needs
## Ren'Py's normal GL renderer (the default on Windows/Mac/Linux).
##
## Hooked up in options.rpy:
##     define config.enter_transition = page_fold_in
##     define config.exit_transition  = page_fold_out


init python:

    ## The turning page. The part of the page past the curl line wraps around
    ## a cylinder, then lies back over itself (we see its back, tinted paper).
    renpy.register_shader("pageturn.curl", variables="""
        uniform float u_curl;
        uniform float u_radius;
        uniform mat4 u_transform;
        attribute vec4 a_position;
        varying float v_shade;
        varying float v_back;
    """, vertex_200="""
        float pt_d = a_position.x - u_curl;
        float pt_nx = a_position.x;
        float pt_th = 0.0;

        if (pt_d > 0.0) {
            pt_th = pt_d / u_radius;
            if (pt_th <= 3.14159265) {
                pt_nx = u_curl + u_radius * sin(pt_th);
            } else {
                pt_nx = u_curl - (pt_d - 3.14159265 * u_radius);
            }
            v_shade = 0.55 + 0.45 * abs(cos(pt_th));
            v_back = pt_th > 1.5707963 ? 1.0 : 0.0;
        } else {
            v_shade = 1.0 - 0.28 * exp(pt_d / (u_radius * 1.4));
            v_back = 0.0;
        }

        gl_Position = u_transform * vec4(pt_nx, a_position.y, a_position.z, a_position.w);
    """, fragment_300="""
        vec3 pt_paper = vec3(0.93, 0.90, 0.82) * gl_FragColor.a;
        vec3 pt_col = mix(gl_FragColor.rgb, pt_paper, v_back * 0.6);
        gl_FragColor = vec4(pt_col * v_shade, gl_FragColor.a);
    """)

    ## Soft shadow cast on the page underneath, next to the curl.
    renpy.register_shader("pageturn.shadow", variables="""
        uniform float u_curl;
        uniform float u_radius;
        attribute vec4 a_position;
        varying float v_ps_x;
    """, vertex_300="""
        v_ps_x = a_position.x;
    """, fragment_300="""
        float ps_dx = v_ps_x - u_curl;
        float ps_vis = clamp((u_curl + u_radius) / u_radius, 0.0, 1.0);
        float ps_s = 0.0;
        if (ps_dx > 0.0) {
            float ps_k = 1.0 - clamp(ps_dx / (u_radius * 2.4), 0.0, 1.0);
            ps_s = 0.55 * ps_k * ps_k * ps_vis;
        }
        gl_FragColor = vec4(gl_FragColor.rgb * (1.0 - ps_s), gl_FragColor.a);
    """)


## Opening the menu: the game page turns away to the left.
##   duration - seconds the turn takes (smaller = faster)
##   radius   - how tightly the page curls, in pixels (bigger = fatter roll)
transform page_fold_in(duration=0.9, radius=130.0, *, new_widget=None, old_widget=None):
    delay duration

    ## The menu, revealed underneath.
    contains:
        new_widget
        events True
        mesh True
        shader "pageturn.shadow"
        u_radius radius
        u_curl (float(config.screen_width))
        ease duration u_curl (-1.2 * radius)

    ## The game page, curling away.
    contains:
        old_widget
        events False
        mesh (200, 2)
        shader "pageturn.curl"
        u_radius radius
        u_curl (float(config.screen_width))
        ease duration u_curl (-1.2 * radius)


## Leaving the menu: the game page turns back over, from the left.
transform page_fold_out(duration=0.9, radius=130.0, *, new_widget=None, old_widget=None):
    delay duration

    ## The menu, covered as the page returns.
    contains:
        old_widget
        events False
        mesh True
        shader "pageturn.shadow"
        u_radius radius
        u_curl (-1.2 * radius)
        ease duration u_curl (float(config.screen_width))

    ## The game page, turning back over it.
    contains:
        new_widget
        events True
        mesh (200, 2)
        shader "pageturn.curl"
        u_radius radius
        u_curl (-1.2 * radius)
        ease duration u_curl (float(config.screen_width))
