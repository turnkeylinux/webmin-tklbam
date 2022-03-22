#!/usr/bin/perl
# save_cron.cgi
# - save cron job status (enabled = executable; disabled = non-executable)

use strict;
use warnings;
require 'tklbam-lib.pl';
our (%in);
ReadParse();

set_cron_daily($in{'enabled'});
redirect('');

webmin_log('save', 'cron', $in{'enabled'} ? 'enabled' : 'disabled', \%in);
