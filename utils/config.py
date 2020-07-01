import os

class Config(object):

    def __init__(self, params, name: str):
        self.__dict__.update(params)
        self.name = name
        self.force = False
        self.additional_cmake_args = []

        self.defaults()
        self.check()

    def check(self):

        # check if all directories exist
        for key in self.__dict__:

            p = self.__dict__[key]

            if key.endswith("path"):
                if not os.path.exists(p):
                    print("[WARNING] %s path does not exist: %s" % (key, p))
                else:
                    tmp = os.path.abspath(p)
                    tmp = tmp.replace("\\", "/")    # cmake has issues with windows path separators
                    self.__dict__[key] = tmp

    def defaults(self):

        # "debug" builds debug and release
        if "buildconfig" not in self.__dict__ or not self.buildconfig:
            self.buildconfig = "debug"

        # call install?
        if "install" not in self.__dict__:
            self.install = True

        # if set to True, we'll run a dry run (only configure cmake)
        if "cmakeonly" not in self.__dict__:
            self.cmakeonly = False

        # if set, we can skip builds
        if "binaryfile" not in self.__dict__:
            self.binaryfile = ""

        if "srcpath" not in self.__dict__ or not self.srcpath:
            self.srcpath = os.path.join(self.repopath, self.name)

        # this is not called 'path' because it won't exist until we call cmake
        if "builddir" not in self.__dict__ or not self.builddir:
            self.builddir = os.path.join(self.repopath, "build")
        else:
            self.builddir = os.path.abspath(self.builddir)

    def cmake_args(self):

        return ""

    def __str__(self):

        keyvals = [key + ": " + str(self.__dict__[key])
                   for key in self.__dict__]
        return "\n".join(keyvals)

    def is_built(self):

        if self.force:
            return False

        return os.path.isfile(self.binaryfile)

def repopath(arg0: str):

    # return "C:/coding/nomacs/nomacs/3rd-party/imageformats"

    relp = os.path.dirname(arg0)
    absp = os.path.abspath(relp)

    # here we assume that this script is in /scripts/src
    rp = os.path.join(absp, os.pardir) 

    return os.path.abspath(rp)
