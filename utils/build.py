
def build(config):
    import subprocess as sp

    if config.project != "all" and config.name not in config.project:
        print(config.name + " not selected for building, skipping...")
        return

    if config.is_built():
        print(config.name + " exists, skipping...")
        return

    print(config.name + " ----------------------------------------------")

    cmakeconfig = "cmake " + " ".join(config.cmake_args())

    print(cmakeconfig)

    # configure
    try:
        sp.run(cmakeconfig, check=True)
    except sp.CalledProcessError:
        print("[ERROR] cmake config failed - aborting...")
        exit(1)

    if config.cmakeonly:
        print("\"cmakeonly\" specified -> done")
        return

    # build release
    sp.run("cmake --build %s --config Release -- -m" %
           (config.builddir), check=True)

    # build debug?!
    if config.buildconfig.lower() == "debug":
        sp.run("cmake --build %s --config Debug -- -m" %
               (config.builddir), check=True)

    # install
    if config.install:
        sp.run("cmake --build %s --config Release --target INSTALL -- -m" %
               (config.builddir), check=True)
