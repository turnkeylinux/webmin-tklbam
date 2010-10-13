#!/usr/bin/perl
require 'tklbam-lib.pl';

ReadParse();

ui_print_header(undef, $module_info{'desc'}, "", undef, 0, 1);

print ui_form_start(undef, "post");
print ui_table_start('Configure Restore -- Backup #1, TurnKey Joomla 90MB', 
'width=100%', 4);

print ui_table_row('Time ago:', ui_textbox('time', '', 40), undef,
["align=right"]);
print ui_table_row(hlink('Escrow key:', 'escrow'),
ui_upload('upload_escrow', 30), undef,
['align=right']);

print ui_table_row('Skip:', 
ui_checkbox('skip_packages', 1, 'New packages') . '<br />' .
ui_checkbox('skip_files', 1, 'Filesystem changes') . '<br />' .
ui_checkbox('skip_database', 1, 'Database'), undef,
["align=right"]
);

print ui_table_row('Limits:', ui_textarea('limits', "", 3, 30), undef,
["align=right"]);

print ui_table_end();

print ui_form_end([[undef, 'Run Restore']]);



ui_print_footer('/', $text{'index'});
