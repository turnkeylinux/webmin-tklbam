#!/usr/bin/perl
use Data::Dumper;
require 'tklbam-lib.pl';

sub print_passphrase_form {
    my ($in) = @_;

    print ui_form_start('restore_run.cgi', 'form-data');

    foreach my $var qw(skpp id 
                       time upload_escrow upload_escrow_filename
                       skip_packages skip_files skip_database limits) {
        print ui_hidden($var, $in->{$var}) if defined $in->{$var};
    }

    my $id = $in->{'id'};
    print ui_table_start("Passphrase Required to Restore Backup #$id");
    print ui_table_row("Passphrase:", 
                       ui_password("passphrase", undef, 20));
    print ui_table_row(undef, ui_submit("Continue"));
    print ui_table_end();

    print ui_form_end();
}

ReadParse(undef, "GET");
ReadParseMime() unless $in{'id'};

my $id = $in{'id'};
my $skpp = $in{'skpp'};
my $passphrase = $in{'passphrase'};
my $key = $in{'upload_escrow'};

validate_cli_args($id, $in{'time'}, $in{'limits'});

if($skpp eq 'yes' and !$passphrase and !$key) {
    ui_print_header(undef, "Passphrase Required", "", undef, 0, 1);
    if(defined($passphrase)) {
        print "Error: passphrase can't be empty<br />";
    }
    print_passphrase_form(\%in);
}

if($skpp eq 'no' or ($passphrase or $key)) {
    ui_print_unbuffered_header(undef, "Restoring Backup #$id ...", "", undef, 0, 0);

    my $command = "tklbam-restore $id --noninteractive";
    my $keyfile;

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
    $command .= " --time='$in{'time'}'" if $in{'time'};
    $command .= " --skip-files" if $in{'skip_files'};
    $command .= " --skip-packages" if $in{'skip_packages'};
    $command .= " --skip-database" if $in{'skip_database'};

    my $error = htmlified_system($command, "$passphrase\n");

    # execute command
    unlink($keyfile) if $keyfile;

    if($error == 11) { # 11 is code for BADPASSPHRASE
        # show passphrase dialog
        print_passphrase_form(\%in);
        
    } else {

        print ui_form_start('index.cgi'), ui_hidden('mode', 'restore'), ui_submit('Back'), ui_form_end();
        unlink($keyfile) if $keyfile;
    }
}

ui_print_footer('/', $text{'index'});
