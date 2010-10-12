BEGIN { push(@INC, ".."); };

use WebminCore;
init_config();

use constant STATUS_OK => 0;
use constant STATUS_NO_BACKUP => 10;
use constant STATUS_NO_APIKEY => 11;

use constant PATH_CRON_DAILY => "/etc/cron.daily/tklbam-backup";

use constant PATH_TKLBAM_CONF => '/etc/tklbam/conf';
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

sub get_escrow {
    my ($path) = @_;
    my $error;
    $retval = execute_command("tklbam-escrow --no-passphrase $path", undef, undef, \$error);
    die "tklbam-escrow error: $error" if $retval != 0;
}

sub get_backup_id {
    my ($exitcode, $output) = tklbam_status();
    return unless ($exitcode == STATUS_OK);

    return ($output =~ /Backup ID #(.*?),/);
}


sub _conf_read {
    open(FH, PATH_TKLBAM_CONF)
        or die "open: $!";

    return join("", <FH>);
}

sub _conf_write {
    my ($conf) = @_;
    open(FH, ">" . PATH_TKLBAM_CONF)
        or die "open: $!";
    print FH $conf;
    close FH;
}

sub _conf_parse {
    my ($conf) = @_;
    my @lines = split(/\n/, $conf);
    my %conf;
    foreach my $line (@lines) {
        $line =~ s/#.*//;
        $line =~ s/^\s+//;
        $line =~ s/\s+$//;
        next if($line eq '');

        my ($key, $val) = split(/\s+/, $line);
        $key =~ s/-/_/g;
        $conf{$key} = $val;
    }
    return \%conf;
}

sub _conf_update_option {
    my ($conf, $key, $val) = @_;
    $key =~ s/_/-/g;
    unless($conf =~ s/^(\s*$key\s+).*/\1$val/gm) {
        $conf .= "\n$key $val\n";
    }
    return $conf;
}

sub _conf_format {
    my ($conf, $parsed) = @_;
    foreach my $key (keys %$parsed) {
        $conf = _conf_update_option($conf, $key, $parsed->{$key});
    }
    return $conf;
}

sub conf_get {
    return _conf_parse(_conf_read());
}

sub conf_set {
    my ($options) = @_;
    my $orig;
    eval {
        $orig = _conf_read();
    };
    if($@) {
        $orig = "";
    }
    _conf_write(_conf_format($orig, $options));
}

1;

