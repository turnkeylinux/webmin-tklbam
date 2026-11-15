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
    print_approval($code);
} elsif (($result->{status} || '') eq 'pending') {
    print '<p>' . text('init_pending') . '</p>';
    print_approval($code);
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

sub print_approval {
    my ($code) = @_;
    print '<p>' . text('init_profile_reason') . '</p>';
    print '<p>' . text('init_approve_link', $code ? '?code=' . $code : '') . '</p>';
    print '<p>' . text('init_return_instruction') . '</p>';
    if ($code) {
        print '<style>details[open] .hub-disclosure-arrow { transform: rotate(90deg); }</style>';
        print '<details style="margin-bottom: 1em"><summary style="cursor: pointer"><span class="hub-disclosure-arrow" style="display: inline-block; margin-right: .4em" aria-hidden="true">&#9654;</span>' . text('init_other_device') . '</summary>';
        print '<p>' . text('init_other_device_instruction') . '</p>';
        print '<p><strong>https://hub.turnkeylinux.org/connect</strong><br>' . text('init_code') . ' <strong>' . html_escape($code) . '</strong></p></details>';
    }
}
