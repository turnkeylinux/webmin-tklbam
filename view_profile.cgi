#!/usr/bin/perl
require 'tklbam-lib.pl';
ReadParse();


$profile_path = profile_path();
ui_print_header("Filesystem backup profile ($profile_path)", "View Backup Profile", "", undef, 0, 0);

$data = read_file_contents($profile_path);

print ui_textarea("data", $data, 20, 80, undef, 1);

ui_print_footer('/', $text{'index'});

