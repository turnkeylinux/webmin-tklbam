#!/usr/bin/perl
require 'tklbam-lib.pl';

sub hidden_data {
    my ($in, @skip) = @_;
    my $buf;
    foreach my $var qw(skpp id force passphrase
                       time upload_escrow upload_escrow_filename
                       skip_packages skip_files skip_database limits) {
        next if grep { $_ eq $var } @skip;
        $buf .= ui_hidden($var, $in->{$var}) if defined $in->{$var};
    }
    return $buf;
}

sub print_passphrase_form {
    my ($in) = @_;

    print ui_form_start('restore_run.cgi', 'form-data');

    print hidden_data($in, "passphrase");

    my $id = $in->{'id'};
    my $escrowkey = $in{'upload_escrow_filename'};
    $escrowkey =~ s|.*/||;

    my $title = ($escrowkey ? 
                 "Passphrase Required for '$escrowkey'" :
                 "Passphrase Required to Restore Backup #$id");

    print ui_table_start($title);
    print ui_table_row("Passphrase:", 
                       ui_password("passphrase", undef, 20));
    print ui_table_row(undef, ui_submit("Continue"));
    print ui_table_end();

    print ui_form_end();
}

sub print_incompatible_force {
    my ($in) = @_;

    print _ui_confirmation_form('restore_run.cgi', 'form-data',
    "Are you sure you want to restore an incompatible backup?",
        undef,
        [ [ 'force', 'Confirm' ],
          [ 'cancel',  'Cancel' ] ], hidden_data($in),
        );

}

ReadParse(undef, "GET");
ReadParseMime() unless $in{'id'};

redirect('?mode=restore') if $in{'cancel'};

#ui_print_header();
#use Data::Dumper;
#print "<pre>" . Dumper(\%in) ."</pre>";

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

    $command .= " --force" if $in{'force'};

    my $error = htmlified_system($command, "$passphrase\n");

    # execute command
    unlink($keyfile) if $keyfile;

    if($error == 11) { # 11 is code for BADPASSPHRASE
        # show passphrase dialog
        print_passphrase_form(\%in);
        
    } elsif($error == 10) { # 10 is code for INCOMPATIBLE
        print_incompatible_force(\%in);
    } else {

        print ui_form_start('index.cgi'), ui_hidden('mode', 'restore'), ui_submit('Back'), ui_form_end();
        unlink($keyfile) if $keyfile;
    }
}

ui_print_footer('/', $text{'index'});
