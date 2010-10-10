BEGIN { push(@INC, ".."); };

use WebminCore;
init_config();

use constant STATUS_OK => 0;
use constant STATUS_NO_BACKUP => 10;
use constant STATUS_NO_APIKEY => 11;

sub is_installed {
    return (`which tklbam` ne '');
}

sub is_initialized {
    my $status = `tklbam-status`;
    my $exitcode = $?;
    $exitcode = $exitcode >> 8 if $exitcode != 0;

    die "couldn't execute tklbam-status: $!" unless defined $status;
    
    if ($exitcode == 0 || $exitcode == STATUS_NO_BACKUP) {
        return 1;
    } elsif ($exitcode == STATUS_NO_APIKEY) {
        return 0;
    }

}

1;

