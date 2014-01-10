"""
    Copyright (c) 2014 Hekar Khani

    This software is provided 'as-is', without any express or implied
    warranty. In no event will the authors be held liable for any damages
    arising from the use of this software.

    Permission is granted to anyone to use this software for any purpose,
    including commercial applications, and to alter it and redistribute it
    freely, subject to the following restrictions:

       1. The origin of this software must not be misrepresented; you must not
       claim that you wrote the original software. If you use this software
       in a product, an acknowledgment in the product documentation would be
       appreciated but is not required.

       2. Altered source versions must be plainly marked as such, and must not be
       misrepresented as being the original software.

       3. This notice may not be removed or altered from any source
       distribution.
"""

from yaml import load, dump
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper
from collections import namedtuple

def database_view_from_file(file):
    DatabaseView = namedtuple('DatabaseView', 'database name language views')
    
    data = load(file, Loader=Loader)
    return DatabaseView(data['database'], data['design'], 
        data['language'], data['views'])
    