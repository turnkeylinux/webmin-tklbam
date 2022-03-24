#!/usr/bin/perl
# options.cgi
# - edit config options

use strict;
use warnings;
our (%in);
require 'tklbam-lib.pl';
ReadParse();

ui_print_header(undef, text('conf_title'), "", undef, 0, 0);

my $conf = conf_get();

print ui_form_start("save_conf.cgi", "post");
print ui_table_start(text('conf_options_title'), undef, 2);

print ui_table_row(
    hlink(
        text('conf_options_volsize'), "volsize"),
        ui_textbox("volsize", $conf->{'volsize'}, 3) . " MBs",
    1);
print ui_table_row(
    hlink(
        text('conf_options_parallel_up'), "s3-parallel-uploads"),
        ui_textbox("s3_parallel_uploads", $conf->{'s3_parallel_uploads'}, 3),
    1);
print ui_table_row(
    hlink(
        text('conf_options_full_backup'), "full-backup"),
        ui_textbox("full_backup", $conf->{'full_backup'}, 3)
        . " Must end with one of: <strong>M</strong> | <strong>W</strong> | <strong>D</strong> (Month|Week|Day)",
    1);
print ui_table_row(
    hlink(
        text('conf_options_skip_files'), "skip-files"),
        ui_yesno_radio("backup_skip_files", $conf->{'backup_skip_files'}, 'True', 'False'),
    1);
print ui_table_row(
    hlink(
        text('conf_options_skip_packages'), "skip-pkgs"),
        ui_yesno_radio("backup_skip_packages", $conf->{'backup_skip_packages'}, 'True', 'False'),
    1);
print ui_table_row(
    hlink(
        text('conf_options_skip_database'), "skip-db"),
        ui_yesno_radio("backup_skip_database", $conf->{'backup_skip_database'}, 'True', 'False'),
    1);
print ui_table_row(
    hlink(
        text('conf_options_restore_cache_size'), "restore-cache-size"),
        ui_textbox("restore_cache_size", $conf->{'restore_cache_size'}, 3)
        . " Must end with one of: <strong>%</strong> | <strong>MB</strong> | <strong>GB</strong> | <strong>TB</strong>",
    1);
print ui_table_row(
    hlink(
        text('conf_options_restore_cache_dir'), "restore-cache-dir"),
        ui_textbox("restore_cache_dir", $conf->{'restore_cache_dir'}, 20),
    1);

print ui_table_end();
print ui_form_end([[undef, text('conf_options_save')]]);
ui_print_footer('', text('index_return'));
