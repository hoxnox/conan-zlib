from nxtools import NxConanFile
from conans import CMake,tools
from glob import glob

class ZlibConan(NxConanFile):
    name = "zlib"
    version = "1.2.11"
    license = ""
    url = "https://github.com/hoxnox/conan-zlib"
    license = "http://zlib.net/zlib_license.html"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared":[True, False]}
    default_options = "shared=False"
    build_policy = "missing"
    description = "A Massively Spiffy Yet Delicately Unobtrusive Compression Library"

    def do_source(self):
        self.retrieve("c3e5e9fdd5004dcb542feda5ee4f0ff0744628baf8ed2dd5d66f8ca1197cb1a1",
                [
                    "vendor://zlib.net/zlib/zlib-{v}.tar.gz".format(v=self.version),
                    "http://zlib.net/zlib-{v}.tar.gz".format(v=self.version)
                ], "zlib-{v}.tar.gz".format(v=self.version))

    def do_build(self):
        cmake = CMake(self)
        tools.untargz("zlib-{v}.tar.gz".format(v=self.version), "{staging_dir}/src".format(staging_dir=self.staging_dir))
        src_dir = "{staging_dir}/src/zlib-{v}".format(staging_dir=self.staging_dir, v=self.version)
        cmake.build_dir = "{src_dir}/build".format(src_dir=src_dir)
        for file in sorted(glob("patch/[0-9]*.patch")):
            self.output.info("Applying patch '{file}'".format(file=file))
            tools.patch(base_path=src_dir, patch_file=file, strip=0)

        cmake_defs = {
                "CMAKE_INSTALL_PREFIX": self.staging_dir,
                "CMAKE_INSTALL_LIBDIR": "lib",
                "INSTALL_STATIC" if self.options.shared else "INSTALL_SHARED" : "OFF",
                "BUILD_SHARED_LIBS": "1" if self.options.shared else "0"
                }
        cmake.verbose = True
        cmake_defs.update(self.cmake_crt_linking_flags())
        cmake.configure(defs=cmake_defs, source_dir=src_dir)
        cmake.build(target="install")

    def do_package_info(self):
        if self.settings.compiler == "Visual Studio":
            self.cpp_info.libs = ["zlib"] if self.options.shared else ["zlibstatic"]
        else:
            self.cpp_info.libs = ["z"]

