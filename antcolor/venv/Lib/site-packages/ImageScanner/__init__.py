#!/usr/bin/env python

import sys

if sys.version_info[0] == 3:
    from Watershed.Watershed import __version__
    from Watershed.Watershed import __author__
    from Watershed.Watershed import __date__
    from Watershed.Watershed import __url__
    from Watershed.Watershed import __copyright__
    from Watershed.Watershed import Watershed
    from ImageScanner.ImageScanner import ImageScanner
else:
    from Watershed import __version__
    from Watershed import __author__
    from Watershed import __date__
    from Watershed import __url__
    from Watershed import __copyright__
    from Watershed import Watershed
    from ImageScanner import ImageScanner



