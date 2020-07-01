from utils.config import Config

class GenericConfig(Config):

    def __init__(self, params, name: str):
        super().__init__(params, name)

        self.install = False

    def defaults(self):

        if "srcpath" not in self.__dict__ or not self.srcpath:
            self.srcpath = os.path.join(self.repopath, self.name)

        # this is not called 'path' because it won't exist until we call cmake
        if "builddir" not in self.__dict__ or not self.builddir:
            self.builddir = os.path.join(self.repopath, "build", self.name)

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

        return os.path.join(self.builddir, "Release", self.name + ".dll")

class ExpatConfig(Config):
    
    def __init__(self, params):
        super().__init__(params, "expat")

        self.install = False

    def defaults(self):
    
        if "srcpath" not in self.__dict__ or not self.srcpath:
            self.srcpath = os.path.join(self.repopath, self.name)

        # this is not called 'path' because it won't exist until we call cmake
        if "builddir" not in self.__dict__ or not self.builddir:
            self.builddir = os.path.join(self.repopath, "build", self.name)

        self.binaryfile = os.path.join(self.builddir, "Release", "expat.dll")

        super().defaults()

    def cmake_args(self):

        # tune cmake parameters here
        args = [
            "--clean-first",
            "-DBUILD_examples=OFF",
            "-DBUILD_tests=OFF",
            "-B" + self.builddir,
            self.srcpath
        ]

        return args

class ExifConfig(Config):

    def __init__(self, params):
        super().__init__(params, "exiv2")

        self.install = False

    def defaults(self):
    
        if "srcpath" not in self.__dict__ or not self.srcpath:
            self.srcpath = os.path.join(self.repopath, self.name)

        if "libpath" not in self.__dict__ or not self.libpath:
            self.libpath = os.path.join(self.repopath, "build")

        # this is not called 'path' because it won't exist until we call cmake
        if "builddir" not in self.__dict__ or not self.builddir:
            self.builddir = os.path.join(self.repopath, "build", self.name)

        self.binaryfile = os.path.join(self.builddir, "Release", "bin", "exiv2.dll")

        super().defaults()

    def cmake_args(self):

        # tune cmake parameters here
        args = [
            "--clean-first",
            "-DEXPAT_BUILD_PATH=" + os.path.join(self.libpath, "expat"),
            "-DEXPAT_INCLUDE_DIR=" + os.path.join(self.repopath, "expat", "lib"),
            "-DZLIB_INCLUDE_DIR=" + os.path.join(self.repopath, "opencv", "3rdparty", "zlib"),
            "-DZLIB_BUILD_PATH=" + os.path.join(self.libpath, "opencv", "3rdparty"),
            "-B" + self.builddir,
            self.srcpath
        ]

        return args

class LibrawConfig(Config):
    
    def __init__(self, params):
        super().__init__(params, "libraw")

        self.install = False

    def defaults(self):
    
        if "srcpath" not in self.__dict__ or not self.srcpath:
            self.srcpath = os.path.join(self.repopath, self.name)

        # this is not called 'path' because it won't exist until we call cmake
        if "builddir" not in self.__dict__ or not self.builddir:
            self.builddir = os.path.join(self.repopath, "build", self.name)

        self.binaryfile = os.path.join(self.builddir, "Release", "raw.dll")

        super().defaults()

    def cmake_args(self):

        # tune cmake parameters here
        args = [
            "--clean-first",
            "-DENABLE_EXAMPLES=OFF",
            "-B" + self.builddir,
            self.srcpath
        ]

        return args

class QuazipConfig(Config):
    
    def __init__(self, params):
        super().__init__(params, "quazip")

        self.install = False

    def defaults(self):
    
        if "srcpath" not in self.__dict__ or not self.srcpath:
            self.srcpath = os.path.join(self.repopath, self.name)

        # this is not called 'path' because it won't exist until we call cmake
        if "builddir" not in self.__dict__ or not self.builddir:
            self.builddir = os.path.join(self.repopath, "build", self.name)

        if "libpath" not in self.__dict__ or not self.libpath:
            self.libpath = os.path.join(self.repopath, "build")



        self.binaryfile = os.path.join(self.builddir, "Release", "quazip5.dll")

        super().defaults()

    def cmake_args(self):

        # tune cmake parameters here
        args = self.additional_cmake_args + [
            "--clean-first",
            "-DCMAKE_PREFIX_PATH=" + self.qtpath,
            "-B" + self.builddir,
            self.srcpath
        ]

        return args

class OpenCVConfig(Config):
    
    def __init__(self, params):
        super().__init__(params, "opencv")

        self.install = False

    def defaults(self):
    
        if "srcpath" not in self.__dict__ or not self.srcpath:
            self.srcpath = os.path.join(self.repopath, self.name)

        # this is not called 'path' because it won't exist until we call cmake
        if "builddir" not in self.__dict__ or not self.builddir:
            self.builddir = os.path.join(self.repopath, "build", self.name)

        # FIXME: release is generated by cmake - so this is not enough to ask for...
        self.binaryfile = os.path.join(self.builddir, "bin", "Release", "opencv_core430.dll")

        super().defaults()

    def cmake_zlib(self):

        args = [
            "-DZLIB_INCLUDE_DIRS=" + os.path.join(self.srcpath, "3rdparty", "zlib"),
            "-DZLIB_BUILD_PATH=" + os.path.join(self.builddir, "3rdparty"),
        ]
 
        return args

    def cmake_args(self):

        # tune cmake parameters here
        args = [
            "--clean-first",
            "-DBUILD_PERF_TESTS=OFF",
            "-DBUILD_TESTS=OFF",
            "-DBUILD_opencv_java=OFF",
            "-DBUILD_opencv_java_bindings_generator=OFF",
            "-DBUILD_opencv_python=OFF",
            "-DBUILD_opencv_apps=OFF",
            "-DBUILD_opencv_dnn=OFF",
            "-DBUILD_opencv_calib3d=OFF",
            "-DBUILD_opencv_highgui=OFF",
            "-DBUILD_opencv_photo=OFF",
            "-DBUILD_opencv_python2=OFF",
            "-DBUILD_opencv_python3=OFF",
            "-DBUILD_opencv_python_tests=OFF",
            "-DBUILD_opencv_python_bindings_generator=OFF",
            "-DBUILD_opencv_stitiching=OFF",
            "-DBUILD_opencv_video=OFF",
            "-DBUILD_opencv_videoio=OFF",
            "-B" + self.builddir,
            self.srcpath
        ]

        return args


def make(params):

    params['install'] = False

    # opencv config
    opencv = OpenCVConfig(params)
    # some script debugging options:
    # opencv.cmakeonly = True
    # opencv.force = True
    # print(opencv)
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
