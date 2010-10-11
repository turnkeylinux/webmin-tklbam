#!/usr/bin/perl
require 'tklbam-lib.pl';

ui_print_header(undef, "Set Passphrase", "", undef, 1, 1);

print ui_form_start(undef, "post");
print ui_table_start("Change Backup Passphrase", undef, 2);
print ui_table_row("New passphrase:", ui_password("passphrase", $in{'apikey'}, 20));
print ui_table_row("New passphrase (again):", ui_password("passphrase_confirm", $in{'apikey'}, 20));
print ui_table_row(undef, "(Leave empty to remove passphrase)", 2);
print ui_table_end();
print ui_form_end([[undef, 'Change']]);

ui_print_footer('/', $text{'index'});

# TODO: confirm passphrase removal
