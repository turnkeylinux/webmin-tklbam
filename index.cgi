#!/usr/bin/perl
# Show all Foobar webserver websites

require 'tklbam-lib.pl';

ui_print_header(undef, $module_info{'desc'}, "", undef, 1, 1);

ui_print_endpage($text{'index_not_installed'}) unless (is_installed());

if (is_initialized()) {
    print "CONF SCREEN HERE";
} else {
    print "ENTER API-KEY";
}

ui_print_footer('/', $text{'index'});
