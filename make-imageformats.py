from utils.config import Config

class FormatsConfig(Config):

    def __init__(self, params, name: str):
        super().__init__(params, name)

    def defaults(self):



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
    # params['cmakeonly'] = True

    # config libde265 which we need for libheif
    libde265 = FormatsConfig(params, "libde265")
    libde265.builddir = os.path.join(libde265.builddir, libde265.name)
    libde265.binaryfile = os.path.join(libde265.builddir, libde265.name, "Release", libde265.name + ".dll")
    build(libde265)
    
    # config libheif
    libheif = FormatsConfig(params, "libheif")
    libheif.builddir = os.path.join(libheif.builddir, libheif.name)
    libheif.binaryfile = os.path.join(libheif.builddir, "libheif", "Release", "heif.dll")
    build(libheif)
    
    # configure image formats
    params["srcpath"] = params["repopath"]
    imageformats = FormatsConfig(params, "imageformats")
    build(imageformats)

    # uncomment for debugging
    # print(libde265)
    # print(libheif)
    # print(imageformats)

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
    parser.add_argument('--build-dir', dest='builddir', type=str, default="",
                        help='Specify the build directory')
    parser.add_argument('--nomacs', action='store_true',
                        help='Specify the build directory')

    # make args a dict
    params = vars(parser.parse_args())

    # configure for in-repo nomacs build
    if params['nomacs']:

        if not params['repopath']:
            params['repopath'] = os.path.join(repopath(sys.argv[0]), "3rd-party", "imageformats")
        if not params['builddir']:
            params['builddir'] = os.path.join(
                repopath(sys.argv[0]), "3rd-party", "build", "imageformats")

    make(params)