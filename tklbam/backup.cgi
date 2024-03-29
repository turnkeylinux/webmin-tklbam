#!/usr/bin/perl
# backup.cgi
# - run backup or simulation

use strict;
use warnings;
require './tklbam-lib.pl';
our (%in);
ReadParse();

my $simulate = 0;
if (defined($in{'simulate'})) {
    $simulate = 1;
}

my $command = "tklbam-backup";
$command .= " --simulate --disable-resume" if $simulate;

ui_print_unbuffered_header(undef, 
                           ($simulate ? "Running Backup Simulation..." : "Running Backup..."), 
                           "", undef, 0, 0);
htmlified_system($command);
cache_expire('list') if !$simulate;
print ui_form_start("index.cgi"), ui_submit("Back"), ui_form_end();

ui_print_footer('/', text('index'));

webmin_log('backup', $simulate ? 'simulate' : 'real', $command, \%in);
