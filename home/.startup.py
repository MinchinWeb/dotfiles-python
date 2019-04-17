"""
Personal Python startup file for Wm Minchin

History:
    2019-04-17  Original Writing
                    - colored prompt
                    - colored tracebacks
"""

import sys
from pprint import pprint

PY2 = sys.version_info[0] == 2
PY3 = sys.version_info[0] == 3

# if PY2:
#     from __future__ import (absolute_import, division, print_function,
#                             with_statement)

try:
    import colorama
except ImportError:
    pass
finally:
    colorama.init()

    # set up colored prompt
    #
    # consider numbering these lines; do this by create a function to generate
    # ps1 and ps2
    sys.ps1 = "{}>>> {}".format(colorama.Fore.GREEN, colorama.Style.RESET_ALL)
    sys.ps2 = "{}... {}".format(colorama.Fore.YELLOW, colorama.Style.RESET_ALL)

# colored tracebacks
try:
    import tbvaccine
except ImportError:
    pass
finally:
    tbvaccine.add_hook(isolate=False)


print()
# http://www.wiseoldsayings.com/python-quotes/
print("Python is executable pseudocode. Perl is executable line noise.")
print("Smile, and have fun! :)")
print()
