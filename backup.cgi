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

foreign_require("proc", "proc-lib.pl");
local ($fh, $pid) = &foreign_call("proc", "pty_process_exec", $command);

print "<b>&gt; $command</b><br />";

$| = 1;

while($line = <$fh>) {
    $line = html_escape($line) . "<br />";
    print $line;
}
close($fh);
waitpid($pid, 0);

print ui_form_start("index.cgi");
print ui_submit("Back", "back");
print ui_form_end();

ui_print_footer('/', $text{'index'});
