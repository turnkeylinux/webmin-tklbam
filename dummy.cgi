#!/usr/bin/perl
use Data::Dumper;
require 'tklbam-lib.pl';

ReadParse();

ui_print_header(undef, $module_info{'desc'}, "", undef, 0, 1);
    print "<pre>" . Dumper(\%in) . "</pre>";
ui_print_footer('/', $text{'index'});
