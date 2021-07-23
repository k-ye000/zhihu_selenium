# dic为录制的实际页面中鼠标x轴移动数据
mouse_move_dic = {
    800: 0.04149377594387229,
    801: 0.3797468351565231,
    802: 0.12345679021430368,
    803: 0.2531645567710154,
    804: 0.125,
    805: 0.25,
    806: 0.5,
    807: 0.375,
    808: 0.625,
    809: 0.375,
    810: 0.6172839510715185,
    811: 0.5,
    812: 0.5063291135420308,
    813: 0.375,
    814: 0.24691358042860737,
    815: 0.25,
    816: 0.041666666666666664,
    817: 0.00694766095395363,
    818: 0.25,
    819: 0.24691358042860737,
    820: 0.25,
    821: 0.125,
    822: 0.0625,
    823: 0.0625,
    824: 0.125,
    825: 0.001968503937007874,
    826: 0.5,
    827: 0.125,
    828: 0,
    829: 0.125,
    830: 0.0004370438354978388,
    831: 0.6329113919275385,
    832: 0.25,
    833: 0.375,
    834: 0.25,
    835: 0.3797468351565231,
    836: 0.375,
    837: 0.25,
    838: 0.37037037064291106,
    839: 0.2531645567710154,
    840: 0.37037037064291106,
    841: 0.375,
    842: 0.375,
    843: 0.375,
    844: 0.3797468351565231,
    845: 0.37037037064291106,
    846: 0.375,
    847: 0.2531645567710154,
    848: 0.24691358042860737,
    849: 0.25,
    850: 0.24691358042860737,
    851: 0.1282051280091892,
    852: 0.25,
    853: 0.12345679021430368,
    854: 0.125,
    855: 0.25,
    856: 0.1265822783855077,
    857: 0.24691358042860737,
    858: 0.125,
    859: 0.25,
    860: 0.24691358042860737,
    861: 0.3846153840275676,
    862: 0.12422360253046151,
    863: 0.2531645567710154,
    864: 0.24691358042860737,
    865: 0.25,
    866: 0.0625,
    867: 0.3797468351565231,
    868: 0.25,
    869: 0.1875,
    870: 0.125,
    871: 0.25,
    872: 0.24691358042860737,
    873: 0.2531645567710154,
    874: 0.375,
    875: 0.25,
    876: 0.24691358042860737,
    877: 0.5,
    878: 0.3797468351565231,
    879: 0.375,
    880: 0.5,
    881: 0.25,
    882: 0.24691358042860737,
    883: 0.2531645567710154,
    884: 0.25,
    885: 0.125,
    886: 0.24691358042860737,
    887: 0,
    888: 0.0625,
    889: 0.125,
    890: 0.08298755188774458,
    891: 0.0625,
    892: 0.125,
    893: 0.0625,
    894: 0.1265822783855077,
    895: 0.0625,
    896: 0.06230529596172488,
    897: 0.0625,
    898: 0.12578616347485888,
    899: 0.062111801265230755,
    900: 0.125,
    901: 0.0625,
    902: 0.0625,
    903: 0.08333333333333333,
    904: 0.08333333333333333,
    905: 0.0062539086926999615,
    906: 0.125,
    907: 0,
    908: 0.1265822783855077,
    909: 0.12345679021430368,
    910: 0.06289308173742944,
    911: 0.00024850894632206757,
    912: 0.24691358042860737,
    913: 0.8641975315001258,
    914: 0.6140350873982514,
}
move_array = []

def generate_move_array():
    for i in mouse_move_dic.values():
        d = int(i * 12)
        if d:
            move_array.append(d)
    return move_array
