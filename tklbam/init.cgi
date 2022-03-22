#!/usr/bin/perl
# init.cgi
# - tklbam-init input API key

use strict;
use warnings;
our (%in);
require 'tklbam-lib.pl';
ReadParse();

redirect('') if is_initialized();

my $init_error = undef;

validate_cli_args($in{'apikey'});

ui_print_header(undef, text('init_title'), "", undef, 0, 1);

print ui_subheading(text('init_apikey_title'));

print "<p>" . text('init_apikey_desc') . "</p>";

print ui_form_start('do_init.cgi', 'post');

print "<b>".text('init_apikey').": </b>", ui_textbox("apikey", $in{'apikey'}, 20);
print ui_submit(text('init_button'), '', 0, '');

print ui_form_end();

print '<br />';
print text("init_about_tklbam");

ui_print_footer('/', text('index'));
