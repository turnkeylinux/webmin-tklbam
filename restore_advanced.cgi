#!/usr/bin/perl
use Data::Dumper;
require 'tklbam-lib.pl';

ReadParseMime();

validate_cli_args($in{'id'}, $in{'time'}, $in{'limits'});

$command = "tklbam-restore $in{'id'}";

if($in{'upload_escrow'}) {
    umask(077);
    $keyfile = transname($in{'upload_escrow_filename'});
    write_file_contents($keyfile, $in{'upload_escrow'});
    $command .= " --keyfile=$keyfile";
}

if($in{'limits'}) {
    $limits = join(" ", split(/\s+/, $in{'limits'}));
    $command .= " --limits='$limits'";
}
$command .= " --time=$in{'time'}" if $in{'time'};
$command .= " --skip-files" if $in{'skip_files'};
$command .= " --skip-packages" if $in{'skip_packages'};
$command .= " --skip-database" if $in{'skip_database'};

ui_print_unbuffered_header(undef, "Restoring Backup #$in{'id'} ...", "", undef, 0, 0);

print "$command";
htmlified_system($command);
print ui_form_start('index.cgi'), ui_hidden('mode', 'restore'), ui_submit('Back'), ui_form_end();

unlink($keyfile) if $keyfile;
ui_print_footer('/', $text{'index'});
