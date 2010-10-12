#!/usr/bin/perl
require 'tklbam-lib.pl';

ReadParse();

ui_print_unbuffered_header(undef, "Executing Backup", "", undef, 0, 0);
$|=1;

my $simulate = 0;
if (defined($in{'simulate'})) {
    $simulate = 1;
}

$command = "tklbam-backup";
$command .= " --simulate" if $simulate;

clean_environment();
open(CMD, "$command 2>&1 < /dev/null |")
    or die "error: $!";

print "<b>&gt; $command</b><br />";

$| = 1;

while($line = <CMD>) {
    $line = html_escape($line) . "<br />";
    print $line;
}

close(CMD);
reset_environment();

ui_print_footer('/', $text{'index'});
