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

from django import forms


class XMLSelectForm(forms.Form):
    url = forms.URLField()
    encoding = forms.ChoiceField(required=False, choices=[
        ('', 'auto detect encoding'),
        ('2143-ordered', '2143-ordered'),
        ('3412-ordered', '3412-ordered'),
        ('ASCII', 'ASCII'),
        ('Big5', 'Big5'),
        ('EUC-JP', 'EUC-JP'),
        ('EUC-KR', 'EUC-KR'),
        ('EUC-TW', 'EUC-TW'),
        ('GB18030', 'GB18030'),
        ('GB2312', 'GB2312'),
        ('HZ-GB-2312', 'HZ-GB-2312'),
        ('IBM855', 'IBM855'),
        ('IBM866', 'IBM866'),
        ('ISO-2022-CN', 'ISO-2022-CN'),
        ('ISO-2022-JP', 'ISO-2022-JP'),
        ('ISO-2022-KR', 'ISO-2022-KR'),
        ('ISO-8859-1', 'ISO-8859-1'),
        ('ISO-8859-2', 'ISO-8859-2'),
        ('ISO-8859-5', 'ISO-8859-5'),
        ('ISO-8859-7', 'ISO-8859-7'),
        ('ISO-8859-8', 'ISO-8859-8'),
        ('KOI8-R', 'KOI8-R'),
        ('LE', 'LE'),
        ('MacCyrillic', 'MacCyrillic'),
        ('SHIFT_JIS', 'SHIFT_JIS'),
        ('TIS-620', 'TIS-620'),
        ('UTF-16 BE', 'UTF-16 BE'),
        ('UTF-16 LE', 'UTF-16 LE'),
        ('UTF-32 BE', 'UTF-32 BE'),
        ('UTF-8', 'UTF-8'),
        ('windows-1250', 'windows-1250'),
        ('windows-1251', 'windows-1251'),
        ('windows-1252', 'windows-1252'),
        ('windows-1253', 'windows-1253'),
        ('windows-1255', 'windows-1255'),
        ])


class SearchForm(forms.Form):
    keyword = forms.CharField(max_length=100)
