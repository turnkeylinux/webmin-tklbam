#!/usr/bin/perl
require 'tklbam-lib.pl';
ReadParse();

error($text{'index_not_installed'}) unless (is_installed());
redirect("init.cgi") unless is_initialized();

#ui_print_header("<tt>".fmt_status()."</tt>", $module_info{'desc'}, "", undef, 0, 1);
ui_print_header(undef, $module_info{'desc'}, "", undef, 0, 1);

@tabs = ( [ 'backup', 'Backup' ],
          [ 'restore', 'Restore' ] );
print ui_tabs_start(\@tabs, 'mode', $in{'mode'} || 'backup');

print ui_tabs_start_tab('mode', 'backup');

printf '<h4>%s</h4>', fmt_status();

push(@links, "passphrase.cgi");
push(@titles, "Set Passphrase");
push(@icons, "images/passphrase.gif");

push(@links, "escrow.cgi");
push(@titles, "Download Escrow Key");
push(@icons, "images/escrow.gif");

push(@links, "edit_conf.cgi");
push(@titles, "Advanced Configuration");
push(@icons, "images/conf.gif");

push(@links, "http://www.turnkeylinux.org/tklbam");
push(@titles, "Online Documentation");
push(@icons, "images/help.gif");

&icons_table(\@links, \@titles, \@icons, 4);

print ui_buttons_start();
print ui_buttons_row('save_cron.cgi', 'Enable daily backup: ', 
                     'Automatic incremental daily backups',
                     undef,
                     &ui_radio("enabled", get_cron_daily() ? "1" : "0",
                        [ [ 1, $text{'yes'} ],
                          [ 0, $text{'no'} ] ]));


print ui_buttons_row('backup.cgi', 'Run Backup', 
                     'Backup this system to cloud storage',
                     undef,
                     ui_submit('Run a Local Simulation', "simulate"));

print ui_buttons_end();

print ui_tabs_end_tab('mode', 'backup');
print ui_tabs_start_tab('mode', 'restore');

if(rollback_exists()) {
    print ui_subheading("Rollback Last Restore");

    print "<table><tr>";
    print ui_form_start('restore_rollback.cgi', 'post');
    print "<td>";
    print "System snapshot from " . rollback_timestamp();
    print ui_submit("Rollback");
    print "</td>";
    print ui_form_end();
    print "</tr></table>";
}

print ui_subheading("Backup List");

$colalign = [undef, undef, undef, undef, undef, undef, 'align="center"'];

print ui_form_start('restore.cgi');
print "<div style='text-align: right; padding-right: 5px'><a>Refresh</a></div>";

@hbrs = tklbam_list();

unless(@hbrs) {
    print "<b>No backups have yet been created</b>";
} else {
    print ui_columns_start(
                ["ID", "Passphrase", "Created", "Updated", "Size (MB)", "Label",
                "Actions"], 100, undef, $colalign);

    foreach $hbr (@hbrs) {
        my $id = $hbr->[0];
        print ui_columns_row([@$hbr, 
                                ui_submit('Restore', "restore_$id" ) . 
                                ui_submit('Advanced', "advanced_$id")],
                              $colalign);
    }

    print ui_columns_end();
}


print ui_form_end();

print ui_tabs_end_tab('mode', 'restore');

ui_print_footer('/', $text{'index'});

