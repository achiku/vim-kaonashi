if exists("g:loaded_vim_kaonashi")
  finish
endif
let g:loaded_vim_kaonashi = 1

let s:save_cpo = &cpo
set cpo&vim


if has('python3')
    command! -nargs=1 Python python3 <args>
    command! -nargs=1 PyFile py3file <args>
elseif has('python')
    command! -nargs=1 Python python <args>
    command! -nargs=1 PyFile pyfile <args>
else
    echo "kaonashi.vim Error: Requires Vim compiled with +python or +python3"
    finish
endif


" Import Python code
execute "Python import sys"
execute "Python sys.path.append(r'" . expand("<sfile>:p:h") . "')"

" Python << EOF
" if 'kaonashi' not in sys.modules:
"     import kaonashi
" else:
"     import imp
"     # Reload python module to avoid errors when updating plugin
"     hackernews = imp.reload(kaonashi)
" EOF

execute "PyFile <sfile>:h:h/plugin/kaonashi.py"

function! KaonashiListNote()
  execute "Python kaonashi.list_notes()"
  noremap <buffer> o :Python kaonashi.get_note()<CR>
  noremap <buffer> d :Python kaonashi.delete_note()<CR>
  au BufRead,BufNewFile *.kaonashi  set filetype=markdown
endfunction

function! KaonashiSaveNote()
  execute "Python kaonashi.update_note()"
  execute "Python kaonashi.refresh_note_list()"
endfunction

function! KaonashiCreateNote()
  execute "Python kaonashi.create_note()"
  execute "Python kaonashi.refresh_note_list()"
endfunction

command! KaonashiSaveNote call KaonashiSaveNote()
command! KaonashiListNote call KaonashiListNote()
command! KaonashiCreateNote call KaonashiCreateNote()

let &cpo = s:save_cpo
unlet s:save_cpo
