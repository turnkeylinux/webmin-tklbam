#!/usr/bin/perl
# do_init.cgi
# - save the initization data

use strict;
use warnings;
our (%in);
require 'tklbam-lib.pl';
ReadParse();

our $init_error = undef;

validate_cli_args($in{'apikey'});

if($in{'apikey'}) {
    eval {
        tklbam_init($in{'apikey'});
        webmin_log('init');
        redirect('');
    };
    if ($@) {
        $init_error = $@;
    }
}

ui_print_header(undef, text('init_title'), "", undef, 0, 1);

print ui_subheading(&text('init_error_title'));
print "<b><pre>$init_error</pre></b>";
print ui_buttons_start();
print ui_buttons_row('init.cgi', text('init_error_button'),
                     text('init_error_button_msg'));
print ui_buttons_end();

ui_print_footer('/', text('index'));
