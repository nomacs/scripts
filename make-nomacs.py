from utils.config import Config

class NmcConfig(Config):

    def __init__(self, params):
        super().__init__(params, "nomacs")

    def defaults(self):

        if not self.libpath:
            self.libpath = self.repopath + "/3rd-party/build"

        if "srcpath" not in self.__dict__ or not self.srcpath:
            self.srcpath = self.repopath + "/ImageLounge"

        # this is not called 'path' because it won't exist until we call cmake
        if "builddir" not in self.__dict__ or not self.builddir:
            self.builddir = self.repopath + "/build"

        super().defaults()

    def cmake_args(self):

        # tune cmake parameters here
        args = [
            "-DCMAKE_PREFIX_PATH=" + self.qtpath,
            "-DDEPENDENCY_PATH=" + self.libpath,
            "-DENABLE_TRANSLATIONS=ON",
            "-DENABLE_HEIF=ON",
            "-DENABLE_AVIF=ON",
            "-DENABLE_INCREMENTER=ON",
            "-B" + self.builddir,
            self.srcpath
        ]

        return args

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
    parser.add_argument('--lib-path', dest='libpath', type=str, default="",
                        help='additional cmake arguments')
    parser.add_argument('--repo-path', dest='repopath', type=str, default="",
                        help='path to the nomacs repository')

    # make args a dict
    params = vars(parser.parse_args())

    # get the repository path
    if not params['repopath']:
        params['repopath'] = repopath(sys.argv[0])


    c = NmcConfig(params)

    # uncomment for debugging
    # print(c)

    build(c)