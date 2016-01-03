if exists("g:loaded_vim_kaonashi")
  finish
endif
let g:loaded_vim_kaonashi = 1

let s:save_cpo = &cpo
set cpo&vim

py3file <sfile>:h:h/plugin/vim_kaonashi.py
python3 import vim

function! KaonashiListNote()
    python3 kaonashi.list_note_titles()
    noremap <buffer> o :python3 kaonashi.get_note()<cr>
endfunction

command! KaonashiListNote call KaonashiListNote()

let &cpo = s:save_cpo
unlet s:save_cpo
