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
ui_print_header(undef, $module_info{'desc'}, "", undef, 0, 1);

    print "<pre>" . Dumper(\%in) . "</pre>";
ui_print_footer('/', $text{'index'});
