#!/usr/bin/perl
# overrides.cgi
# - view and edit overrides file

use strict;
use warnings;
our (%in);
require 'tklbam-lib.pl';
ReadParse();

my $overrides_path = get_overrides_path();
my $data = read_file_contents($overrides_path);

ui_print_header(undef, text('conf_title'), "", undef, 0, 0);

if(profile_exists()) {
    print text('conf_overrides_profile', 'view_profile.cgi') . '<br />';
}

# Show the file contents
print ui_form_start("save_overrides.cgi", "form-data");
print ui_hidden("file", $overrides_path),"\n";
print ui_textarea("data", $data, 20, 80),"\n";
print ui_form_end([[undef, text('conf_overrides_save')]]);

ui_print_footer("", text('index_return'));
