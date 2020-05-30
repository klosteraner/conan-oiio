from conans import ConanFile, CMake, tools
from conans.errors import ConanException


class OiioConan(ConanFile):
    name = "oiio"
    version = "2.1"
    license = "3-clause BSD"
    author = "Larry Gritz & other contributors"
    url = "https://github.com/OpenImageIO/oiio"
    description = "OpenImageIO provides simple but powerful ImageInput and ImageOutput APIs that abstract the reading and writing of 2D image file formats. They don’t support every possible way of encoding images in memory, but for a reasonable and common set of desired functionality, they provide an exceptionally easy way for an application using the APIs support a wide — and extensible — selection of image formats without knowing the details of any of these formats."
    topics = ("Image", "IO")
    settings = "os", "compiler", "build_type", "arch"
    options = {

        ###
        #  C++ compiler and build process:
        ##

        "VERBOSE":			[True, False],
        "STOP_ON_WARNING": 		[True, False],

        # CMAKE_BUID_TYPE: 		Is set via self.settings.build_type
        # MYCC / MYCXX: 		Set in the conan profile by setting compiler, 
        #				compiler.version and setting CC/CXX in [env]
        # CMAKE_CXX_STANDARD: 		Set via self.settings.compiler.cppstd [Conan standard], 
        #				oiio default is 11
        # USE_LIBCPLUSPLUS: 		Set via self.settings.compiler.libcxx=libc++ 
        #				if self.settings.compiler is set to (apple-)clang
        #"GLIBCXX_USE_CXX11_ABI": 	Is activated via self.settings.compiler.libcxx=libstdc++11 
        #				for gcc/clang/sun-cc

        #TODO: Add additional tooling/options step by step later on:
        # If possible prefer valuelist over "ANY" - to only except valid values
        # Also consider NOT adding dev tools as options of the package when binary remains unchanged

        #"OPENIMAGEIO_SITE" : 		"ANY",
        #"EXTRA_CPP_ARGS":		"ANY",
        #"USE_NINJA":	[True, False],
        #"USE_CCACHE":			[True, False],
        #"CODECOV":                     [True, False], #TODO: Also integrate into tests() 
        # TODO: "c++: error: unrecognized command line option ‘-ftest-coverage -fprofile-arcs -O0’"

        #"SANITIZE":			"ANY", # TODO: Check whether valuelist is more suited
        #"CLANG_TIDY":			[True, False],
        #"CLANG_FORMAT_INCLUDES":	"ANY",
        #"CLANG_TIDY_CHECKS":		"ANY",
        #"CLANG_TIDY_ARGS":		"ANY",
        #"CLANG_TIDY_FIX":		[True, False],
        #"CLANG_FORMAT_EXCLUDES":	"ANY",

        ###
        #  Linking and libraries:
        ##

        "SOVERSION":			"ANY", #TODO: Replace by  valid value list
        "OIIO_LIBNAME_SUFFIX":		"ANY",
        #BUILD_SHARED_LIBS: Is set via self.options.shared below [Conan standard]
        "shared": 			[True, False],
        "LINKSTATIC": 			[True, False],

        ###
        # Optional dependencies
        ##

        # The straight-forward way is to use dependencies via conan,
        # i.e. path hint via <Package>_ROOT not needed.
        # Use direct cmake mechanism in case you want to use non-conan dependencies
        # 
        # Disabling optional dependendies can be handled with below settings
        # Note that cmake disables dependency automatically if not found

        "ENABLE_DCMTK":			[True, False],
        "ENABLE_FFmpeg":		[True, False],
        "ENABLE_Field3D":		[True, False],
        "ENABLE_Freetype":		[True, False],
        "ENABLE_GIF":			[True, False],
        "ENABLE_JPEGTurbo":		[True, False],
        "ENABLE_LibRaw":		[True, False],
        "ENABLE_OpenColorIO":		[True, False],
        "ENABLE_OpenCV":		[True, False],
        "ENABLE_OpenGL":		[True, False],
        "ENABLE_OpenJpeg":		[True, False],
        "ENABLE_OpenVDB":		[True, False],
        "ENABLE_PTex":			[True, False],
        "ENABLE_R3DSDK":		[True, False],
        "ENABLE_TBB":			[True, False],
        "ENABLE_TIFF":			[True, False],
        "ENABLE_Webp":			[True, False],

        #TODO: "USE_EXTERNAL_PUGIXML": Investigate using non-conan dependencies

        #"USE_QT": QT is currently default activated if found in externalpackages.cmake

        #TODO: 	Currently min pybind cannot be retrieved by conan
        #	Set USE_PYTHON=False until this works
	"USE_PYTHON": 			[False],
        #"PYTHON_VERSION":		"ANY", # TODO: Check whether valuelist is more suited

        # Currently the nuke dependency is not clearly documented and google didnt help, don't add for now
        #"USE_NUKE":			[True, False],
        #"NUKE_VERSION":			"ANY", # TODO: Check whether valuelist is more suited

        ###
        #  OIIO build-time options:
        ##

        # INSTALL_PREFIX: Makes no sense for conan package
        "NAMESPACE":			"ANY",
        "EMBEDPLUGINS":			[True, False],
        "OIIO_THREAD_ALLOW_DCLP": 	[True, False],
        "OIIO_BUILD_TOOLS": 		[True, False],
        "OIIO_BUILD_TESTS":		[True, False],
        "BUILD_OIIOUTIL_ONLY":		[True, False],
        "USE_SIMD":			"ANY",
        "TEX_BATCH_SIZE":		"ANY",
        #TODO: Check whether BUILD_MISSING_DEPS can be omitted
        #TODO: Check whether/how TEST regex can be done

        #  Other (Found in Makefile):

        "PYLIB_LIB_PREFIX":		[True, False],
        "PYLIB_INCLUDE_SONAME":		[True, False],
        # DEBUG, PROFILE, RelWithDebInfo will be chosen as setting
        # USE_CPP: Double check how to implement this properly
    }
    default_options = {


        #  C++ compiler and build process:

        "VERBOSE":			False,
        "STOP_ON_WARNING": 		False, #OIIO DEFAULT: True
        #"OPENIMAGEIO_SITE":		None,
        #"EXTRA_CPP_ARGS":		None,
        #"USE_NINJA":			False,
        #"USE_CCACHE":			True,
        #"CODECOV":			False,
        #"SANITIZE":			None,
        #"CLANG_TIDY":			False,
        #"CLANG_FORMAT_INCLUDES":	None,
        #"CLANG_TIDY_CHECKS":		None,
        #"CLANG_TIDY_ARGS":		None,
        #"CLANG_TIDY_FIX":		False,
        #"CLANG_FORMAT_EXCLUDES":	None,

        #  Linking and libraries:
        
        "SOVERSION":  			None,
        "OIIO_LIBNAME_SUFFIX":		None,
        "shared": 			True,
        "LINKSTATIC":			True, #OIIO DEFAULT: False,

        # Optional components: 

        "ENABLE_DCMTK":			True,
        "ENABLE_FFmpeg":		True,
        "ENABLE_Field3D":		True,
        "ENABLE_Freetype":		True,
        "ENABLE_GIF":			True,
        "ENABLE_JPEGTurbo":		True,
        "ENABLE_LibRaw":		True,
        "ENABLE_OpenColorIO":		True,
        "ENABLE_OpenCV":		True,
        "ENABLE_OpenGL":		True,
        "ENABLE_OpenJpeg":		True,
        "ENABLE_OpenVDB":		True,
        "ENABLE_PTex":			True,
        "ENABLE_R3DSDK":		True,
        "ENABLE_TBB":			True,
        "ENABLE_TIFF":			True,
        "ENABLE_Webp":			True,

        "USE_PYTHON":			False, #OIIO DEFAULT: True, see options above for details

        #  OIIO build-time options:

        "NAMESPACE":			None,
        "EMBEDPLUGINS":			True,
        "OIIO_THREAD_ALLOW_DCLP":	True,
        "OIIO_BUILD_TOOLS":		False, #OIIO DEFAULT: True
        "OIIO_BUILD_TESTS":		False, #OIIO DEFAULT: True
        "BUILD_OIIOUTIL_ONLY":		False,
        "USE_SIMD":			None,
        "TEX_BATCH_SIZE":		None,

        #  Other (Found in Makefile):

        "PYLIB_LIB_PREFIX":		False, #TODO: Check actual value
        "PYLIB_INCLUDE_SONAME":		False, #TODO: Check actual value

    }
    generators = "cmake"
    source_folder = 'oiio'

    def configure_cmake(self):
        cmake = CMake(self)
        cmake.definitions["CMAKE_CXX_FLAGS"]="-std=c++0x"

        ###
        #  C++ compiler and build process:
        ##

        if self.options.VERBOSE:
            cmake.definitions["VERBOSE"] = 1 	# verbose cmake
            cmake.verbose = True		# verbose make, set by conan via CMAKE_VERBOSE_MAKEFILE
        #TODO: Add/Check enabling verbose flag for ninja, tests

        if not self.options.STOP_ON_WARNING:
            cmake.definitions["STOP_ON_WARNING"] = 0

        #TODO: Add OPENIMAGEIO_SITE

        #if self.options.EXTRA_CPP_ARGS:
        #    cmake.definitions["EXTRA_CPP_ARGS"] = self.options.EXTRA_CPP_ARGS

        #TODO: Add USE_NINJA

        #if not self.options.USE_CCACHE:
        #    cmake.definitions["USE_CCACHE"] = 0

        #if self.options.CODECOV:
        #    if self.settings.build_type == "Release":
        #        raise ConanException("Code coverage can only be active in debug mode. Set build_type = Debug") 
        #    cmake.definitions["CODECOV"] = 1

        #if self.options.SANITIZE:
        #    cmake.definitions["SANITIZE"] = self.options.SANITIZE

        #if self.options.CLANG_TIDY:
        #    cmake.definitions["CLANG_TIDY"] = 1

        #if self.options.CLANG_FORMAT_INCLUDES:
        #    cmake.definitions["CLANG_FORMAT_INCLUDES"] = self.options.CLANG_FORMAT_INCLUDES

        #if self.options.CLANG_TIDY_CHECKS:
        #    cmake.definitions["CLANG_TIDY_CHECKS"] = self.options.CLANG_TIDY_CHECKS

        #if self.options.CLANG_TIDY_ARGS:
        #    cmake.definitions["CLANG_TIDY_ARGS"] = self.options.CLANG_TIDY_ARGS

        #if self.options.CLANG_TIDY_FIX:
        #    cmake.definitions["CLANG_TIDY_FIX"] = 1

        #if self.options.CLANG_FORMAT_EXCLUDES:
        #    cmake.definitions["CLANG_FORMAT_EXCLUDES"] = self.options.CLANG_FORMAT_EXCLUDES

        ###
        #  Linking and libraries:
        ##

        if self.options.SOVERSION:
            cmake.definitions["SOVERSION"] = self.options.SOVERSION

        if self.options.OIIO_LIBNAME_SUFFIX:
            cmake.definitions["OIIO_LIBNAME_SUFFIX"] = self.options.OIIO_LIBNAME_SUFFIX

        if self.options.LINKSTATIC:
            cmake.definitions["LINKSTATIC"] = 0

        ###
        # Optional dependencies: 
        ##

        # All dependencies are by default enabled (and automatically disabled if not found)

        if not self.options.ENABLE_DCMTK:
            cmake.definitions["ENABLE_DCMTK"] = self.options.ENABLE_DCMTK

        if not self.options.ENABLE_FFmpeg:
            cmake.definitions["ENABLE_FFmpeg"] = self.options.ENABLE_FFmpeg

        if not self.options.ENABLE_Field3D:
            cmake.definitions["ENABLE_Field3D"] = self.options.ENABLE_Field3D

        if not self.options.ENABLE_Freetype:
            cmake.definitions["ENABLE_Freetype"] = self.options.ENABLE_Freetype 

        if not self.options.ENABLE_GIF:
            cmake.definitions["ENABLE_GIF"] = self.options.ENABLE_GIF 

        if not self.options.ENABLE_JPEGTurbo:
            cmake.definitions["ENABLE_JPEGTurbo"] = self.options.ENABLE_JPEGTurbo

        if not self.options.ENABLE_LibRaw:
            cmake.definitions["ENABLE_LibRaw"] = self.options.ENABLE_LibRaw

        if not self.options.ENABLE_OpenColorIO:
            cmake.definitions["ENABLE_OpenColorIO"] = self.options.ENABLE_OpenColorIO

        if not self.options.ENABLE_OpenCV:
            cmake.definitions["ENABLE_OpenCV"] = self.options.ENABLE_OpenCV

        if not self.options.ENABLE_OpenGL:
            cmake.definitions["ENABLE_OpenGL"] = self.options.ENABLE_OpenGL

        if not self.options.ENABLE_OpenJpeg:
            cmake.definitions["ENABLE_OpenJpeg"] = self.options.ENABLE_OpenJpeg

        if not self.options.ENABLE_OpenVDB:
            cmake.definitions["ENABLE_OpenVDB"] = self.options.ENABLE_OpenVDB

        if not self.options.ENABLE_PTex:
            cmake.definitions["ENABLE_PTex"] = self.options.ENABLE_PTex

        if not self.options.ENABLE_R3DSDK:
            cmake.definitions["ENABLE_R3DSDK"] = self.options.ENABLE_R3DSDK 

        if not self.options.ENABLE_TBB:
            cmake.definitions["ENABLE_TBB"] = self.options.ENABLE_TBB

        if not self.options.ENABLE_TIFF:
            cmake.definitions["ENABLE_TIFF"] = self.options.ENABLE_TIFF

        if not self.options.ENABLE_Webp:
            cmake.definitions["ENABLE_Webp"] = self.options.ENABLE_Webp

        if not self.options.USE_PYTHON:
            cmake.definitions["USE_PYTHON"]=self.options.USE_PYTHON

        ###
        #  OIIO build-time options:
        ##

        if self.options.NAMESPACE:
            cmake.defitions["NAMESPACE"]=self.options.NAMESPACE

        if not self.options.EMBEDPLUGINS:
            cmake.definitions["EMBEDPLUGINS"]=0

        if not self.options.OIIO_THREAD_ALLOW_DCLP:
            cmake.definitions["OIIO_THREAD_ALLOW_DCLP"]=0

        if not self.options.OIIO_BUILD_TOOLS:
            cmake.definitions["OIIO_BUILD_TOOLS"] = 0

        if not self.options.OIIO_BUILD_TESTS:
            cmake.definitions["OIIO_BUILD_TESTS"] = 0

        if self.options.BUILD_OIIOUTIL_ONLY:
            cmake.definitions["BUILD_OIIOUTIL_ONLY"] = 1

        if self.options.USE_SIMD:
            cmake.definitions["USE_SIMD"] = self.options.USE_SIMD

        if self.options.TEX_BATCH_SIZE:
            cmake.definitions["TEX_BATCH_SIZE"] = self.options.TEX_BATCH_SIZE

        print("build folder", self.build_folder)
        cmake.configure(source_folder="oiio")
        return cmake

    def source(self):
        self.run("git clone https://github.com/OpenImageIO/oiio.git")
	# oiio already has conan_basic_setup() included in root CMakeLists.txt

    def requirements(self):
        self.requires("zlib/1.2.11")
        self.requires("libtiff/4.0.9")
        self.requires("libpng/1.6.37")
        self.requires("openexr/2.4.0")
        self.requires("boost/1.70.0")
        self.requires("libjpeg/9d")
        self.requires("libjpeg-turbo/2.0.2")
        self.requires("giflib/5.1.4")
        self.requires("freetype/2.10.0")
        self.requires("opencv/4.1.1@conan/stable")
        self.requires("openjpeg/2.3.1")
        self.requires("tsl-robin-map/0.6.1@tessil/stable")
        self.requires("tbb/2020.0")
        #TODO:
        #self.requires("opencolorio? not on conan?")
        #self.requires("pybind11/2.4.3 - conan doesn't have this minimum version")
        #self.requires("dcmtk")
        #self.requires("ffmpeg")
        #self.requires("field3d")
        #self.requires("libheif")
        #self.requires("libraw")
        #self.requires("openvdb")
        #self.requires("ptex")
        #self.requires("qt5")
        #self.requires("libsquish")

    def build(self):
        cmake = self.configure_cmake()
        cmake.verbose = True
        cmake.build()


    def package(self):
        cmake = self.configure_cmake()
        # double check if source folder is still the same in the export
        cmake.install()
        #TODO: Copy license
        #self.copy("*.h", dst="include", src="hello")
        #self.copy("*hello.lib", dst="lib", keep_path=False)
        #self.copy("*.dll", dst="bin", keep_path=False)
        #self.copy("*.so", dst="lib", keep_path=False)
        #self.copy("*.dylib", dst="lib", keep_path=False)
        #self.copy("*.a", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ["OpenImageIO"]

