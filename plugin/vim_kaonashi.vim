if exists("g:loaded_vim_kaonashi")
  finish
endif
let g:loaded_vim_kaonashi = 1

let s:save_cpo = &cpo
set cpo&vim

py3file <sfile>:h:h/plugin/vim_kaonashi.py
python3 import vim

function! KaonashiHello(name)
  python3 kaonashi.greeting(vim.eval('a:name'))
endfunction

function! KaonashiListNote()
  python3 kaonashi.list_note_titles()
endfunction

command! -nargs=1 KaonashiHello call KaonashiHello(<f-args>)
command! KaonashiListNote call KaonashiListNote()

let &cpo = s:save_cpo
unlet s:save_cpo
