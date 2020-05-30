#include <iostream>
#include <OpenImageIO/imageio.h>

using namespace OIIO;

int main() 
{
    const char *filename = "test.jpg";
    const int xres = 640, yres = 480;
    const int channels = 3;  // RGB
    unsigned char pixels[xres*yres*channels];

    std::unique_ptr<ImageOutput> out = ImageOutput::create(filename);
    if (! out)
        return 1;
    ImageSpec spec (xres, yres, channels, TypeDesc::UINT8);
    out->open (filename, spec);
    out->write_image (TypeDesc::UINT8, pixels);
    out->close ();

    return 0;
}
