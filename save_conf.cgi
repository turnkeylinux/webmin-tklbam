#!/usr/bin/perl
use Data::Dumper;
require 'tklbam-lib.pl';

ReadParse();
error_setup("Conf options");

conf_set({'volsize' => $in{'volsize'},
         'full_backup' => $in{'full_backup'}});

redirect('edit_conf.cgi');
