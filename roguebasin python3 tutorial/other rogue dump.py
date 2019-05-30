'''#font stuff, tcod specific
  font_path = 'arial10x10.png' # pathname starts from here rogue.py is
  font_flags = libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD # the lay out may change if I change the font file
  libtcod.console_set_custom_font(font_path, font_flags)

  #setting up the window_width
  window_title = 'Python 3 Roguelike Tutorial'
  fullscreen = False
  libtcod.console_init_root(constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT, window_title, fullscreen)

  # if we want real-time play, otherwise this just isn;t used if we are turn based
  libtcod.sys_set_fps(constants.LIMIT_FPS)'''

  '''# set text to white (the 0 is the console we're printing to (the screen))
    libtcod.console_set_default_foreground(0, libtcod.white)

    # print the @ at coors (1, 1) (again, the first 0 is the screen)
    libtcod.console_put_char(0, 1, 1, '@', libtcod.BKGND_NONE)

    # at the end of the main loop, we need to present the changes made to the screen. This is called 'flushing the console'
    libtcod.console_flush()'''
