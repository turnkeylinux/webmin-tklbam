#!/usr/bin/perl
require 'tklbam-lib.pl';

error($text{'index_not_installed'}) unless (is_installed());

redirect("init.cgi") unless is_initialized();
ReadParse();
if(defined($in{'cron_daily_submit'})) {
    set_cron_daily($in{'cron_daily'});
}

ui_print_header(undef, $module_info{'desc'}, "", undef, 1, 1);

print ui_form_start();

print ui_table_start("Daily automatic backups", undef, 2);
print ui_table_row(ui_checkbox("cron_daily", 1, "Enabled", get_cron_daily()), 
                   ui_submit("Save", "cron_daily_submit"));
print ui_table_end();

print ui_form_end();



ui_print_footer('/', $text{'index'});
