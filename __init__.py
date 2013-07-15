# -*- coding: utf-8 -*-

import os

__all__ = ["PiCam"]

class PiCam(object):
    PHOTOCMD = "raspistill"
    VIDEOCMD = "raspivid"

    def __init(self, path=None):
        if path:
            path = os.expandvars(os.expanduser(path))
            os.chdir(path)
        self.path = path

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
         
        target = name
        if path:
            path = os.expandvars(os.expanduser(path))
            target = os.path.join(path, name)
        
        parts = [mode, "-o %s -t %s" % (target, timeout)]
        for key, value in kwargs.items():
            if isinstance(value, bool):
            	if value:
                    parts.append("--%s" % key)
            else:
                parts.append("--%s %s" % (key, value))
        
        cmd = " ".join(parts)
        os.system(cmd)
    
    def photo(self, *args, **kwargs):
        self.__record(PiCam.PHOTOCMD, *args, **kwargs)

    def video(self, name=None, path=None, **kwargs):
        self.__record(PiCam.VIDEOCMD, *args, **kwargs)
        