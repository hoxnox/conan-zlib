#include "zlib.h"

int main(int argc, char **argv)
{
    z_stream strm;
    strm.zalloc = Z_NULL;
    strm.zfree = Z_NULL;
    strm.opaque = Z_NULL;
    if (deflateInit(&strm, 1) != Z_OK)
        return -1;
    return 0;
}

