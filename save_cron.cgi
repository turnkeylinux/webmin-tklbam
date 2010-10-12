#!/usr/bin/perl
require 'tklbam-lib.pl';

use Data::Dumper;
ReadParse();
ui_print_header(undef, $module_info{'desc'}, "", undef, 1, 1);
print "<pre>" . Dumper(\%in) . "</pre>";
ui_print_footer('/', $text{'index'});
