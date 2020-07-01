from utils.config import Config

class FormatsConfig(Config):

    def __init__(self, params, name: str):
        super().__init__(params, name)

    def defaults(self):

        if "srcpath" not in self.__dict__ or not self.srcpath:
            self.srcpath = os.path.join(self.repopath, self.name)

        # this is not called 'path' because it won't exist until we call cmake
        if "builddir" not in self.__dict__ or not self.builddir:
            self.builddir = os.path.join(self.repopath, "build")

        super().defaults()

    def cmake_args(self):

        # tune cmake parameters here
        args = [
            "--clean-first",
            "-DCMAKE_PREFIX_PATH=" + 
                os.path.join(self.builddir, "libde265") + ";" +
                os.path.join(self.builddir, "libheif") + ";" +
                self.qtpath,
            "-B" + self.builddir,
            self.srcpath
        ]

        return args

def make(params):

    params['install'] = False

    # config libde265 which we need for libheif
    libde265 = FormatsConfig(params, "libde265")
    libde265.builddir = os.path.join(libde265.builddir, libde265.name)
    libde265.binaryfile = os.path.join(libde265.builddir, "Release", libde265.name + ".dll")

    # config libheif
    libheif = FormatsConfig(params, "libheif")
    libheif.builddir = os.path.join(libheif.builddir, libheif.name)
    libheif.binaryfile = os.path.join(libheif.builddir, "libheif", "Release", "heif.dll")
    
    # configure image formats
    imageformats = FormatsConfig(params, "imageformats")
    imageformats.srcpath = imageformats.repopath

    # uncomment for debugging
    # print(libde265)
    # print(libheif)
    print(imageformats)

    build(libde265)
    build(libheif)
    build(imageformats)

if __name__ == "__main__":
    import argparse
    import sys
    import os
    
    from utils.config import repopath
    from utils.make import build

    parser = argparse.ArgumentParser(
        description='packs nomacs portable.')

    parser.add_argument("qtpath", type=str,
                        help="""path to your Qt folder""")
    parser.add_argument('--repo-path', dest='repopath', type=str, default="",
                        help='path to the nomacs repository')
    parser.add_argument('--build-config', dest='buildconfig', type=str, default="",
                        help='build configuration [debug|release]')

    # make args a dict
    params = vars(parser.parse_args())

    # get the repository path
    if not params['repopath']:
        params['repopath'] = repopath(sys.argv[0])

    make(params)
