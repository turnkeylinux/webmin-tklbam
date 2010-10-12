#!/usr/bin/perl
require 'tklbam-lib.pl';

ui_print_header(undef, "Advanced Configuration", "", undef, 0, 0);

@tabs = ( [ 'conf', 'Options' ],
          [ 'overrides', 'Overrides' ] );
print ui_tabs_start(\@tabs, 'mode', 'conf');

# configuration options
print ui_tabs_start_tab('mode', 'conf');

print ui_form_start("save_conf.cgi", "post");
print ui_table_start("Configuration Options", undef, 2);

print ui_table_row(hlink("Size of backup volumes", "volsize"), ui_textbox("volsize", "50", 3) . " MBs", 1);

print ui_table_row(hlink("Frequency of full backup", "full-backup"), ui_textbox("full_backup", "1M", 3), 1);

print ui_table_end();
print ui_form_end([[undef, 'Save Options']]);

print ui_tabs_end_tab('mode', 'conf');

# overrides
print ui_tabs_start_tab('mode', 'overrides');

$overrides_path = get_overrides_path();
print ui_form_start("save_overrides.cgi", "post");
print ui_table_start("Backup Overrides ($overrides_path)");

$data = read_file_contents($overrides_path);

print "Overrides the <b><a>default profile</a></b><br />";
print ui_textarea("data", $data, 20, 80),"\n";
print ui_table_end();
print ui_form_end([[undef, 'Save Overrides']]);

print ui_tabs_end_tab('mode', 'overrides');
print ui_tabs_end();

ui_print_footer('/', $text{'index'});
