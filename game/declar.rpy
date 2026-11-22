define intro_dissolve = Dissolve (3.0)
define flashbang = Dissolve (0.3)
define flash_dissolve = Dissolve(0.2)
transform bg_slow_fadein:
    alpha 0.0
    ease 5.0 alpha 1.0

define narc = Character(
    None,
    kind=nvl,
    what_text_align=0.5,
    what_slow_cps=25,
    what_slow_abortable=True
)

define un = Character("???")
define n = Character(" ")
define ad = Character("Adelaide")
define tm = Character("“Towering man”")
define cr = Character("Crowley")
define narrator = nvl_narrator  
define narNvl = Character('', kind=nvl, color="#c8ffc8")

