#!/usr/bin/perl
# Show all Foobar webserver websites

require 'tklbam-lib.pl';

error($text{'index_not_installed'}) unless (is_installed());

redirect("init.cgi") unless is_initialized();

ui_print_header(undef, $module_info{'desc'}, "", undef, 1, 1);

if (is_initialized()) {
    print "CONF SCREEN HERE";
} else {
    print 
}

ui_print_footer('/', $text{'index'});
