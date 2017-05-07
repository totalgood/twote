from __future__ import print_function, unicode_literals, division, absolute_import
from future import standard_library
standard_library.install_aliases()  # noqa
from builtins import *  # noqa

import re


re_hashtag = r'([-\s!?.;]|^)(#[A-Za-z]{2,32})\b'
cre_hashtag = re.compile(re_hashtag)
re_atuser = r'([-\s!?.;]|^)(@[A-Za-z_0-9]{2,32})\b'
cre_atuser = re.compile(re_atuser)
re_hashtag_at_end = r'.*\s([#][A-Za-z]{2,32})\s*[.?!-=\s]{0,8}\s*$'
cre_hashtag_at_end = re.compile(re_hashtag_at_end)


# regular expression for PyCon 2017 openspaces room numbers at the Oregon Convention Center
re_room = r'([a-zA-Z](\d{3})[-+]?(\d{3})?)'
cre_room = re.compile(re_room)
# TODO: use this regex and process groups separately to normalize room # number string
re_room_liberal = r'([a-zA-Z])[-\s+:,#\\/._]{0,2}(\d{3})[-\s+:,]{0,2}(\d{3})?)'
cre_room_liberal = re.compile(re_room_liberal)
