#!/usr/bin/perl
use Data::Dumper;
require 'tklbam-lib.pl';

ReadParse(\%getin, "GET");
if($getin{'id'}) {
    # got here from a one-step restore

    ui_print_header(undef, "Restoring Backup #$in{'id'} ...", "", undef, 0, 0);
    print "simple restore";
    print "<pre>" . Dumper(\%getin) . "</pre>";
    ui_print_footer('/', $text{'index'});
    exit;

} else {
    # got here from an advanced restore

    ReadParseMime();

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

    ui_print_unbuffered_header(undef, "Restoring Backup #$in{'id'} ...", "", undef, 0, 0);

    print "$command";
    #htmlified_system($command);
    print ui_form_start('index.cgi'), ui_hidden('mode', 'restore'), ui_submit('Back'), ui_form_end();

    unlink($keyfile) if $keyfile;
    ui_print_footer('/', $text{'index'});

    exit;

    if($skpp eq 'yes') {
        ui_print_header(undef, "Passphrase Required", "", undef, 0, 1);
        print ui_form_start('', "post");
        print ui_hidden("$op:$id:$skpp", "Foo");
        print ui_table_start("Passphrase Required to Restore Backup #$id");
        print ui_table_row("Passphrase:", ui_password("passphrase",
        undef, 20)), ui_table_row(undef, ui_submit("Continue"));
        
        print ui_table_end();
        #print ui_form_end([[undef, 'Continue']]);
        print ui_form_end();
    }
}
