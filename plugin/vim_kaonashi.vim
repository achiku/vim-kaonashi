if exists("g:loaded_vim_kaonashi")
  finish
endif
let g:loaded_vim_kaonashi = 1

let s:save_cpo = &cpo
set cpo&vim

py3file <sfile>:h:h/plugin/vim_kaonashi.py
python3 import vim

function! KaonashiListNote()
  python3 kaonashi.list_notes()
  noremap <buffer> o :python3 kaonashi.get_note()<CR>
  noremap <buffer> d :python3 kaonashi.delete_note()<CR>
  au BufRead,BufNewFile *.kaonashi  set filetype=markdown
endfunction

function! KaonashiSaveNote()
  python3 kaonashi.update_note()
endfunction

function! KaonashiCreateNote()
  python3 kaonashi.create_note()
endfunction

command! KaonashiSaveNote call KaonashiSaveNote()
command! KaonashiListNote call KaonashiListNote()
command! KaonashiCreateNote call KaonashiCreateNote()

let &cpo = s:save_cpo
unlet s:save_cpo
