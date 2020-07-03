import os
from utils.config import Config



def make(params):
    from utils.make import build

    params['install'] = False

    opencv = OpenCVConfig(params)
    # some script debugging options:
    # opencv.cmakeonly = True
    # opencv.force = True
    print(opencv)
    build(opencv)

    # Exiv2
    expat = ExpatConfig(params)
    build(expat)
    
    exiv2 = ExifConfig(params)
    exiv2.additional_cmake_args = opencv.cmake_zlib()
    build(exiv2)

    # libraw
    libraw = LibrawConfig(params)
    build(libraw)

    # quazip
    quazip = QuazipConfig(params)
    quazip.additional_cmake_args = opencv.cmake_zlib()
    build(quazip)

    # uncomment for debugging
    # print(expat)


if __name__ == "__main__":
    import argparse
    import sys
    
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
    parser.add_argument('--configure', action='store_true',
                        help='configure only')

    # make args a dict
    params = vars(parser.parse_args())

    if params['configure']:
        params['cmakeonly'] = True
        params['force'] = True

    # get the repository path
    if not params['repopath']:
        params['repopath'] = os.path.join(repopath(sys.argv[0]), "3rd-party")

    make(params)
