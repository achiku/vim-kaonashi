# -*- coding: utf-8 -*-


def test_list_note():
    from ..vim_kaonashi import Kaonashi
    k = Kaonashi()
    k.list_note_titles()


def test_note():
    from ..vim_kaonashi import Kaonashi
    k = Kaonashi()
    k.note()
