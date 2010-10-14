#!/usr/bin/perl
use Data::Dumper;
require 'tklbam-lib.pl';

sub print_passphrase_form {
    my ($id, $skpp) = @_;

    print ui_form_start('restore_run.cgi', 'form-data');
    print ui_hidden('id', $id);
    print ui_hidden('skpp', $skpp);
    print ui_table_start("Passphrase Required to Restore Backup #$id");
    print ui_table_row("Passphrase:", 
                       ui_password("passphrase", undef, 20));
    print ui_table_row(undef, ui_submit("Continue"));
    print ui_table_end();

    print ui_form_end();
}

ReadParse(undef, "GET");
ReadParseMime() unless $in{'id'};

ui_print_header(undef, "Debug");
print "<pre>" . Dumper(\%in) . "</pre>";

# got here from a one-step restore
my $id = $in{'id'};
my $skpp = $in{'skpp'};
my $passphrase = $in{'passphrase'};

validate_cli_args($id);

if(defined($passphrase) and !$passphrase) {
    print "Error: passphrase can't be empty<br />";
}

if($skpp eq 'yes' and !$passphrase) {
    ui_print_header(undef, "Passphrase Required", "", undef, 0, 1);
    print_passphrase_form($id, $skpp);
}

if($skpp eq 'no' or $passphrase) {
    ui_print_unbuffered_header(undef, "Restoring Backup #$id ...", "", undef, 0, 0);

    my $command = "tklbam-restore $id";
    my $error = htmlified_system($command, $passphrase);

    if($error) {
        # show passphrase dialog
        print "Incorrect passphrase, try again<br />";
        print_passphrase_form($id, $skpp);
        
    } else {

        print ui_form_start('index.cgi'), ui_hidden('mode', 'restore'), ui_submit('Back'), ui_form_end();
        unlink($keyfile) if $keyfile;
    }
}

ui_print_footer('/', $text{'index'});
exit;

# got here from an advanced restore


ui_print_header(undef, "Restoring Backup #$in{'id'} ...", "", undef, 0, 0);
print "advanced restore";
print "<pre>" . Dumper(\%in) . "</pre>";
ui_print_footer('/', $text{'index'});
exit;

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

# execute command
unlink($keyfile) if $keyfile;

exit;
