#!/usr/bin/perl
use Data::Dumper;
require 'tklbam-lib.pl';

ReadParse();

redirect('?mode=restore') if $in{'cancel'};

unless($in{'confirmed'}) {
    
    ui_print_header(undef, "Confirm Rollback", "", undef, 0, 0);

    print ui_confirmation_form('', 
    'DATA LOSS WARNING: This will rollback your system to the pre-restore snapshot from ' .
    rollback_timestamp(),
    
        undef,
        [ [ 'confirmed', 'Confirm Rollback' ],
          [ 'cancel',  'Cancel' ] ], undef
        
        );

    ui_print_footer('/', $text{'index'});
    exit;

}

$timestamp = rollback_timestamp();
$command = "tklbam-restore-rollback --force";
ui_print_unbuffered_header(undef, "Running Rollback...", "", undef, 0, 0);
htmlified_system($command);
print "Rolled back to snapshot from $timestamp<br />";
print ui_form_start('index.cgi'), ui_hidden('mode', 'restore'), ui_submit('Back'), ui_form_end();
ui_print_footer('/', $text{'index'});
