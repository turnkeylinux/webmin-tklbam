#!/usr/bin/perl
use strict;
use warnings;
our (%in);
require 'tklbam-lib.pl';
ReadParse();
my ($result, $failure);
my $action = $in{'action'} || '';
my $code = $in{'code'} || '';
$code = '' unless $code =~ /^[A-Z0-9]{4}-[A-Z0-9]{4}$/;
if ($action eq 'start' || $action eq 'poll') {
    eval { $result = hub_command('connect --' . $action); };
    $failure = $@ if $@;
} else {
    $failure = text('init_unknown_error');
}
if ($result && ($result->{connection_status} || '') eq 'linked') {
    redirect('init.cgi');
}
ui_print_header(undef, text('init_title'), "", undef, 0, 1);
print ui_subheading(text('init_connect_title'));
if ($failure) {
    print '<p>' . html_escape($failure) . '</p>';
} elsif ($action eq 'start') {
    $code = $result->{user_code} || '';
    $code = '' unless $code =~ /^[A-Z0-9]{4}-[A-Z0-9]{4}$/;
    print '<p>' . text('init_approve_desc') . '</p>';
    print '<p><strong>' . $code . '</strong></p>';
    print '<p>' . text('init_approve_link') . '</p>';
} elsif (($result->{status} || '') eq 'pending') {
    print '<p>' . text('init_pending') . '</p>';
    print '<p><strong>' . html_escape($code) . '</strong></p>' if $code;
    print '<p>' . text('init_approve_link') . '</p>';
} else {
    print '<p>' . text('init_expired') . '</p>';
}
if (!$failure && ($action eq 'start' || ($result->{status} || '') eq 'pending')) {
    print ui_form_start('connect.cgi', 'post');
    print ui_hidden('action', 'poll');
    print ui_hidden('code', $code) if $code;
    print ui_submit(text('init_check_button'));
    print ui_form_end();
}
print '<p><a href="init.cgi">' . text('init_back') . '</a></p>';
ui_print_footer('/', text('index'));
