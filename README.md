README for conan-oiio
======================

This is a wrapper to create conan packages of [*OpenImageIO*](https://github.com/OpenImageIO/oiio)

A package can be created using the standard conan workflow:

1. Provide profile (or use default one) for settings
2. Adjust options in the conanfile.py or via the commandline to your needs
3. Run conan create . <user>/<channel>

or a suitable variant (conan create --help).

## Requirements:

The latest stable of conan from pip python package manager works.

## TODO:

- Check oldest version of compatible conan

- Choice on settings of dependencies / Propagation of settings to dependencies

## Conan Recipe License

NOTE: The conan recipe license applies only to the files of this recipe, which can be used to build and package opencv.
It does *not* in any way apply or is related to the actual software being packaged.

[MIT](LICENSE)
