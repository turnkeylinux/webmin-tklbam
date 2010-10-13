#!/usr/bin/perl
require 'tklbam-lib.pl';

ReadParse();

ui_print_unbuffered_header(undef, "Executing Backup", "", undef, 0, 0);

my $simulate = 0;
if (defined($in{'simulate'})) {
    $simulate = 1;
}

$command = "tklbam-backup";
$command .= " --simulate" if $simulate;

htmlified_system($command);

print ui_form_start("index.cgi"), ui_submit("Back", "back"), ui_form_end();

ui_print_footer('/', $text{'index'});
