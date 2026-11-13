#!/usr/bin/perl
use strict;
use warnings;
our (%in);
require 'tklbam-lib.pl';
ReadParse();
redirect('') if is_initialized();

my ($status, $failure);
if (has_command('turnkey-hub')) {
    eval { $status = hub_command('status --local'); };
} else {
    $status = { connection_status => 'legacy' };
}
$failure = $@ if $@;
ui_print_header(undef, text('init_title'), "", undef, 0, 1);
print ui_subheading(text('init_setup_title'));
if ($failure) {
    print '<p>' . html_escape($failure) . '</p>';
    print '<p>' . text('init_retry_page') . '</p>';
} elsif (($status->{connection_status} || '') eq 'legacy') {
    print '<p>' . text('init_legacy_desc') . '</p>';
    print ui_form_start('do_init.cgi', 'post');
    print '<label>' . text('init_legacy_key') . ' ' . ui_textbox('apikey', '', 20) . '</label> ';
    print ui_submit(text('init_button'));
    print ui_form_end();
} elsif (($status->{connection_status} || '') ne 'linked') {
    print '<p>' . text('init_connect_desc') . '</p>';
    print ui_form_start('connect.cgi', 'post');
    print ui_hidden('action', 'start');
    print ui_submit(text('init_connect_button'));
    print ui_form_end();
} else {
    print '<p>' . text('init_setup_desc') . '</p>';
    print ui_form_start('do_init.cgi', 'post');
    print ui_submit(text('init_button'));
    print ui_form_end();
}
print text('init_about_tklbam');
ui_print_footer('/', text('index'));
