#!/usr/bin/perl
use strict;
use warnings;
our (%in);
require 'tklbam-lib.pl';
ReadParse();
my $failure;
eval {
    if (!has_command('turnkey-hub')) {
        die "Enter your Hub API key.\n" unless ($in{'apikey'} || '') =~ /^[A-Z2-7]+$/;
        tklbam_init($in{'apikey'});
    } else {
        tklbam_init();
    }
    webmin_log('init');
    redirect('');
};
$failure = $@ if $@;
$failure =~ s/Then run tklbam-backup again\./Then return here and select Initialize backups./g if $failure;
ui_print_header(undef, text('init_title'), "", undef, 0, 1);
print ui_subheading(text('init_error_title'));
print '<pre style="white-space: pre-wrap">' . html_escape($failure || text('init_unknown_error')) . '</pre>';
print '<p>' . text('init_error_button_msg') . '</p>';
print ui_form_start('init.cgi', 'get');
print ui_submit(text('init_error_button'));
print ui_form_end();
ui_print_footer('/', text('index'));
