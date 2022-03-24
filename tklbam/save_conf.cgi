#!/usr/bin/perl
# save_conf.cgi
# - save config file

use strict;
use warnings;
our (%in);
require 'tklbam-lib.pl';
ReadParse();

error_setup("Conf save error");

if ($in{'volsize'} !~ /^\d+$/) {
    error("invalid volume size '$in{'volsize'}'");
}

if ($in{'s3_parallel_uploads'} !~ /^\d+$/) {
    error("invalid s3 parallel uploads '$in{'s3_parallel_uploads'}'");
}

if ($in{'full_backup'} !~ /^\d+[MWD]$/) {
    error("invalid full backup frequency '$in{'full_backup'}'");
}

if ($in{'backup_skip_files'} !~ /^(?:False|True)$/) {
    error("invalid backup skip files value '$in{'backup_skip_files'}'")
}
# I haven't validated other bools - shouldn't need it

if (($in{'restore_cache_size'} !~ /^\d+%$/) &&
    ($in{'restore_cache_size'} !~ /^\d+[MGT]B$/)) {
        error("invalid restore cache size '$in{'restore_cache_size'}'");
}

if (! -d ($in{'restore_cache_dir'})) {
    error("invalid restore cache dir '$in{'restore_cache_dir'}'")
}

conf_set({'volsize' => $in{'volsize'},
          's3_parallel_uploads' => $in{'s3_parallel_uploads'},
          'full_backup' => $in{'full_backup'},
          'backup_skip_files' => $in{'backup_skip_files'},
          'backup_skip_packages' => $in{'backup_skip_packages'},
          'backup_skip_database' => $in{'backup_skip_database'},
          'restore_cache_size' => $in{'restore_cache_size'},
          'restore_cache_dir' => $in{'restore_cache_dir'} });


redirect('options.cgi');

webmin_log('save', 'conf', undef, \%in);
