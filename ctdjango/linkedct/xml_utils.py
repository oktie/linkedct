#
# Copyright 2009-2015 Oktie Hassanzadeh
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

"""
Implements:
 convert_tex_to_utf8: converts latex symbols into UTF8 encodings.

"""

import re

_utf8enc2latex_mapping_simple = {
    # found in uft8enc.dfu (LaTeX)
    u'&': '\&',
    u'\u00A0': r'~',
    u'\u00C0': r'\`A',
    u'\u00C1': r'\A',
    u'\u00C2': r'\^A',
    u'\u00C3': r'\~A',
    u'\u00C4': r'\"A',
    u'\u00C5': r'\r A',
    u'\u00C6': r'\AE',
    u'\u00C7': r'\c C',
    u'\u00C8': r'\`E',
    u'\u00C9': r'\E',
    u'\u00CA': r'\^E',
    u'\u00CB': r'\"E',
    u'\u00CC': r'\`I',
    u'\u00CD': r'\I',
    u'\u00CE': r'\^I',
    u'\u00CF': r'\"I',
    u'\u00D0': r'\DH',
    u'\u00D1': r'\~N',
    u'\u00D2': r'\`O',
    u'\u00D3': r'\O',
    u'\u00D4': r'\^O',
    u'\u00D5': r'\~O',
    u'\u00D6': r'\"O',
    u'\u00D7': r'\texttimes',
    u'\u00D8': r'\O',
    u'\u00D9': r'\`U',
    u'\u00DA': r'\U',
    u'\u00DB': r'\^U',
    u'\u00DC': r'\"U',
    u'\u00DD': r'\Y',
    u'\u00DE': r'\TH',
    u'\u00DF': r'\ss',
    u'\u00E0': r'\`a',
    u'\u00E1': r'\a',
    u'\u00E2': r'\^a',
    u'\u00E3': r'\~a',
    u'\u00E4': r'\"a',
    u'\u00E5': r'\r a',
    u'\u00E6': r'\ae',
    u'\u00E7': r'\c c',
    u'\u00E8': r'\`e',
    u'\u00E9': r'\'e',
    u'\u00EA': r'\^e',
    u'\u00EB': r'\"e',
    u'\u00EC': r'\`i',
    u'\u00ED': r'\i',
    u'\u00EE': r'\^\i',
    u'\u00EF': r'\"\i',
    u'\u00F0': r'\dh',
    u'\u00F1': r'\~n',
    u'\u00F2': r'\`o',
    u'\u00F3': r'\o',
    u'\u00F4': r'\^o',
    u'\u00F5': r'\~o',
    u'\u00F6': r'\"o',
    u'\u00F7': r'\textdiv',
    u'\u00F8': r'\o',
    u'\u00F9': r'\`u',
    u'\u00FA': r'\u',
    u'\u00FB': r'\^u',
    u'\u00FC': r'\"u',
    u'\u00FD': r'\y',
    u'\u00FE': r'\th',
    u'\u00FF': r'\"y',
    u'\u0102': r'\u A',
    u'\u0103': r'\u a',
    u'\u0104': r'\k A',
    u'\u0105': r'\k a',
    u'\u0106': r'\a\'C',
    u'\u0107': r'\'c',
    u'\u010C': r'\vC',
    u'\u010D': r'\vc',
    u'\u010E': r'\vD',
    u'\u010F': r'\vd',
    u'\u0110': r'\DJ',
    u'\u0111': r'\dj',
    u'\u0118': r'\k E',
    u'\u0119': r'\k e',
    u'\u011A': r'\vE',
    u'\u011B': r'\ve',
    u'\u011E': r'\u G',
    u'\u011F': r'\u g',
    u'\u0130': r'\.I',
    u'\u0131': r'\i',
    u'\u0139': r'\L',
    u'\u013A': r'\l',
    u'\u013D': r'\vL',
    u'\u013E': r'\vl',
    u'\u0141': r'\L',
    u'\u0142': r'\l',
    u'\u0143': r'\N',
    u'\u0144': r'\n',
    u'\u0147': r'\vN',
    u'\u0148': r'\vn',
    u'\u014A': r'\NG',
    u'\u014B': r'\ng',
    u'\u0150': r'\H O',
    u'\u0151': r'\H o',
    u'\u0152': r'\OE',
    u'\u0153': r'\oe',
    u'\u0154': r'\R',
    u'\u0155': r'\r',
    u'\u0158': r'\vR',
    u'\u0159': r'\vr',
    u'\u015A': r'\S',
    u'\u015B': r'\s',
    u'\u015E': r'\c S',
    u'\u015F': r'\c s',
    u'\u0160': r'\vS',
    u'\u0161': r'\vs',
    u'\u0162': r'\c T',
    u'\u0163': r'\c t',
    u'\u0164': r'\vT',
    u'\u0165': r'\vt',
    u'\u016E': r'\r U',
    u'\u016F': r'\r u',
    u'\u0170': r'\H U',
    u'\u0171': r'\H u',
    u'\u0178': r'\"Y',
    u'\u0179': r'\Z',
    u'\u017A': r'\z',
    u'\u017B': r'\.Z',
    u'\u017C': r'\.z',
    u'\u017D': r'\vZ',
    u'\u017E': r'\vz',
}

_latex2utf8enc_mapping_simple = {}
for unicode_char in _utf8enc2latex_mapping_simple.keys():
    _latex2utf8enc_mapping_simple[
        _utf8enc2latex_mapping_simple[unicode_char]] = unicode_char


def convert_tex_to_utf8(source):
    """Converts a string with latex symbols into utf8 encoded string."""
    source = source.replace('{', '').replace('}', '')
    for latex_entity in _latex2utf8enc_mapping_simple.keys():
        source = source.replace(latex_entity,
                                _latex2utf8enc_mapping_simple[latex_entity])
    return source


def preprocess_xml(source):
    #source = convert_tex_to_utf8(source)
    #source = strip_commands(source)
    source = fix_white_space(source)
    source = source.replace('{{', '{')
    source = source.replace('}}', '}')
    return source


def fix_white_space(source):

    def _tilde2wsp(hit):
        return hit.group(0)[0] + ' '

    ttable = [(r'\ ', ' '),
              (r'\!', ' '), ]
    for a, b in ttable:
        source = source.replace(a, b)
    wsp_tilde = re.compile(r'[^/\\]~')
    return wsp_tilde.sub(_tilde2wsp, source).replace('\~', '~')


def strip_commands(source):
    oldstyle_cmd = re.compile(r'{\\[a-zA-Z]{2,}')
    newstyle_cmd = re.compile(r'\\[a-zA-Z]+{')
    source = oldstyle_cmd.sub('{', source)
    source = newstyle_cmd.sub('{', source)
    return source


def split_multiple(value):
    """Used to split multiple terms separated by comma (e.g. keywords)."""
    result = list()
    for item in value.split(','):
        item = item.strip()
        if item:
            result.append(item)
    return result
