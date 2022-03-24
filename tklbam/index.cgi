#!/usr/bin/perl
# index.cgi
# - main tklbam page

use strict;
use warnings;
require './tklbam-lib.pl';
our (%in, %module_info);
ReadParse();

error(text('index_not_installed')) unless (is_installed());
redirect('init.cgi') unless is_initialized();

ui_print_header(undef, $module_info{'desc'}, "", undef, 0, 1);

# Show category icons
my @links = ( "passphrase.cgi", "escrow.cgi",
              "options.cgi", "overrides.cgi",
              "https://www.turnkeylinux.org/tklbam" );
my @titles = ( text('index_setpass'), text('index_download_escrow'),
               text('index_options'), text('index_backup_overrides'),
               text('index_online_docs') );
my @icons = ( "images/passphrase.gif", "images/escrow.gif",
              "images/conf.gif", "images/conf.gif",
              "images/help.gif");
icons_table(\@links, \@titles, \@icons, 5);

my @tabs = ( [ 'backup', text('index_backup') ],
             [ 'restore', text('index_restore') ] );

print ui_tabs_start(\@tabs, 'mode', $in{'mode'} || 'backup');

print ui_tabs_start_tab('mode', 'backup');

printf '<h4>%s</h4>', fmt_status();

print ui_buttons_start();
print ui_buttons_row('save_cron.cgi', text('index_enable_daily'), 
                     text('index_enable_daily_desc'),
                     undef,
                     ui_radio("enabled", get_cron_daily() ? "1" : "0",
                              [ [ 1, text('yes') ],
                                [ 0, text('no') ] ]));

print ui_buttons_row('backup.cgi', text('index_runbackup'), 
                     text('index_runbackup_desc'),
                     undef,
                     "");

print ui_buttons_row('backup.cgi?simulate=true', text('index_runbackup_simulate'),
                     text('index_runbackup_simulate_desc'),
                     undef,
                     "");

print ui_buttons_end();

print ui_tabs_end_tab('mode', 'backup');
print ui_tabs_start_tab('mode', 'restore');

if(rollback_exists()) {
    print ui_subheading(text('index_rollback_title'));

    print "<table><tr>";
    print ui_form_start('restore_rollback.cgi', 'post');
    print "<td>";
    print text('index_rollback_timestamp', rollback_timestamp());
    print ui_submit(text('index_rollback'));
    print "</td>";
    print ui_form_end();
    print "</tr></table>";
}

print ui_subheading(text('index_list'));

my $colalign = [undef, undef, undef, undef, undef, undef, 'align="center"'];

print ui_form_start('restore.cgi', 'post');
printf "<div style='text-align: right; padding-right: 5px'><a href='list_refresh.cgi'>%s</a></div>", text('index_list_refresh');

my @hbrs = tklbam_list();
my @this_hbr;
my $backup_id = get_backup_id();
if ($backup_id) {
    @this_hbr = tklbam_list($backup_id);
}

unless(@hbrs) {
    print '<b>'.text('index_list_nobackups').'</b>';
} else {
    my @backup_list_tabs = ( [ 'this_server', text('index_list_local') ],
                             # [ 'this_type', text('index_list_type') ],
                             [ 'all_backups', text('index_list_all') ] );

    print ui_tabs_start(\@backup_list_tabs, 'list_backups', 'this_server', 0);

    print ui_tabs_start_tab('list_backups', 'this_server');
    if ($backup_id) {
        show_backups(@this_hbr);
    } else {
        print "<p>No backups for this server.</p>";
        print "<p>Please either create a backup, or select 'All backups' tab (above) to display all Hub backups.<p>";
    }
    print ui_tabs_end_tab('list_backups', 'this_server');

    #print ui_tabs_start_tab('list_backups', 'this_type');
    #print "<p>NOT IMPLEMENTED YET</p>";
    #print ui_tabs_end_tab('list_backups', 'this_type');

    print ui_tabs_start_tab('list_backups', 'all_backups');
    show_backups(@hbrs);
    print ui_tabs_end_tab('list_backups', 'all_backups');

    print ui_tabs_end();
}


print ui_form_end();

print ui_tabs_end_tab('mode', 'restore');
print ui_tabs_end();

ui_print_footer('/', text('index'));
