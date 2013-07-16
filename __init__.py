# -*- coding: utf-8 -*-

import os, random

__all__ = ["PiCam"]

class PiCam(object):
    PHOTOCMD = "raspistill"
    VIDEOCMD = "raspivid"

    def __init__(self, path=None, shortargs=False):
        if path:
            path = os.expandvars(os.expanduser(path))
            os.chdir(path)
        self.path = path
        self.shortargs = shortargs

    def help(self, mode):
        if mode.lower() == "photo":
            mode = PiCam.PHOTOCMD
        elif mode.lower() == "video":
            mode = PiCam.VIDEOCMD
        else:
            return
        os.system("%s --help" % mode)

    def __record(self, mode, name=None, path=None, timeout=0, **kwargs):
        if mode not in [PiCam.PHOTOCMD, PiCam.VIDEOCMD]:
            raise Exception("unknown mode: '%s'" % mode)
        
        if not name:
            name = "img_%s.jpg" % random.randint(1, 1000)
        target = name
        if path:
            path = os.expandvars(os.expanduser(path))
            target = os.path.join(path, name)
        
        parts = [mode, "-o %s -t %s" % (target, timeout)]
        indicator = "-" if self.shortargs else "--"
        for key, value in kwargs.items():
            if isinstance(value, bool):
            	if value:
                    parts.append("%s%s" % (indicator, key))
            else:
                parts.append("%s%s %s" % (indicator, key, value))
        
        cmd = " ".join(parts)
        os.system(cmd)
    
    def photo(self, *args, **kwargs):
        self.__record(PiCam.PHOTOCMD, *args, **kwargs)

    def video(self, *args, **kwargs):
        self.__record(PiCam.VIDEOCMD, *args, **kwargs)
        
