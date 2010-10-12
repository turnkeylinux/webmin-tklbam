BEGIN { push(@INC, ".."); };

use WebminCore;
init_config();

use constant STATUS_OK => 0;
use constant STATUS_NO_BACKUP => 10;
use constant STATUS_NO_APIKEY => 11;

use constant PATH_CRON_DAILY => "/etc/cron.daily/tklbam-backup";
use constant PATH_TKLBAM_OVERRIDES => "/etc/tklbam/overrides";

sub is_installed {
    return has_command("tklbam");
}

sub is_initialized {
    my ($exitcode, undef) = tklbam_status();
    
    if ($exitcode == STATUS_OK || $exitcode == STATUS_NO_BACKUP) {
        return 1;
    } elsif ($exitcode == STATUS_NO_APIKEY) {
        return 0;
    }
}

sub fmt_status {
    my ($exitcode, $output) = tklbam_status();
    if ($exitcode == STATUS_NO_APIKEY) {
        return "NOT INITIALIZED";
    } elsif ($exitcode == STATUS_NO_BACKUP) {
        return "No backups have yet been created.";
    } else {
        chomp $output;
        $output =~ s/.*?:\s+//;
        return $output;
    }
}

sub tklbam_status {
    my $output = backquote_command("tklbam-status --short");
    my $exitcode = $?;
    $exitcode = $exitcode >> 8 if $exitcode != 0;

    die "couldn't execute tklbam-status: $!" unless defined $output;

    return ($exitcode, $output)
}

sub tklbam_init {
    my ($apikey) = @_;
    $output = backquote_command("tklbam-init $apikey 2>&1");
    die $output if $? != 0;
}

sub get_cron_daily {
    return (-x PATH_CRON_DAILY);
}

sub set_cron_daily {
    my ($flag) = @_;
    if ($flag) {
        unless (-e PATH_CRON_DAILY) {
            open(FH, ">" . PATH_CRON_DAILY) 
                or die "can't open file: " . PATH_CRON_DAILY;

            print FH "#!/bin/sh\n";
            print FH "tklbam-backup --quiet\n";
            close FH;
        }
        chmod 0755, PATH_CRON_DAILY;
    } else {
        chmod 0644, PATH_CRON_DAILY;
    }
}

sub get_overrides_path {
    return PATH_TKLBAM_OVERRIDES;
}

sub set_passphrase {
    my ($passphrase) = @_;
    my $output;
    my $error;
    my $retval = execute_command("tklbam-passphrase", \$passphrase, \$output, \$error);
    die "tklbam-passphrase error: $error" if $retval != 0;
}

1;

