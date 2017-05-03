from nxtools import NxConanFile
from conans import CMake,tools


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
        cmake.build_dir = "{staging_dir}/src".format(staging_dir=self.staging_dir)
        tools.untargz("zlib-{v}.tar.gz".format(v=self.version), cmake.build_dir)
        cmake.configure(defs={
                "CMAKE_INSTALL_PREFIX": self.staging_dir,
                "CMAKE_INSTALL_LIBDIR": "lib",
                "BUILD_SHARED_LIBS": "1" if self.options.shared else "0"
            }, source_dir="zlib-{v}".format(v=self.version))
        cmake.build(target="install")

    def do_package_info(self):
        if self.settings.compiler == "Visual Studio":
            self.cpp_info.libs = ["zlib"] if self.options.shared else ["zlibstatic"]
        else:
            self.cpp_info.libs = ["z"] if self.options.shared else ["z.a"]

