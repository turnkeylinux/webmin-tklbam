#!/usr/bin/perl
# list_refresh.cgi
# - refresh list

use strict;
use warnings;
require 'tklbam-lib.pl';

cache_expire('list');
redirect('?mode=restore');
