#!/usr/bin/perl
require 'tklbam-lib.pl';

error($text{'index_not_installed'}) unless (is_installed());
redirect("init.cgi") unless is_initialized();

ui_print_header(undef, $module_info{'desc'}, "", undef, 1, 1);
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
print ui_buttons_row('save_cron.cgi', 'Enable daily backup:', 
                     'Automatic incremental daily backups',
                     undef,
                     &ui_radio("enabled", 1,
                        [ [ 1, $text{'yes'} ],
                          [ 0, $text{'no'} ] ]));

print ui_buttons_row('backup.cgi', 'Backup now', 'Run a backup of this
system right now');

print ui_buttons_end();

print ui_hr();
print "<b>Last backup:</b> " . fmt_status();


ui_print_footer('/', $text{'index'});
