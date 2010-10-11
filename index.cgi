#!/usr/bin/perl
require 'tklbam-lib.pl';

error($text{'index_not_installed'}) unless (is_installed());

redirect("init.cgi") unless is_initialized();
ReadParse();
if(defined($in{'cron_daily'})) {
    set_cron_daily($in{'cron_daily'});
}

ui_print_header(undef, $module_info{'desc'}, "", undef, 1, 1);

print ui_form_start(undef);

print ui_table_start("Configuration", undef, 2);
print ui_table_row("Daily backups", ui_yesno_radio("cron_daily", get_cron_daily()));

print ui_form_end([[undef, 'Apply']]);

ui_print_footer('/', $text{'index'});
