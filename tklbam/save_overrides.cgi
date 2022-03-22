#!/usr/bin/perl
# save_overrides.cgi
# - save overrides file data

use strict;
use warnings;
our (%in);
require 'tklbam-lib.pl';
error_setup(text('conf_overrides_err'));
ReadParseMime();

my $overrides_path = get_overrides_path();
my $data = "$in{'data'}\n"; # enusre that there is always a trailing newline
$data =~ s/\r//g;
$data =~ s/\n+$/\n/; # ensure that there is only one trailing newline
$data =~ /\S/ || error(text('conf_overrides_err_msg'));
write_file_contents($overrides_path, $data);

webmin_log('save', 'overrides', undef, \%in);
redirect('');
