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

unless(@hbrs) {
    print '<b>'.text('index_list_nobackups').'</b>';
} else {
    print ui_columns_start( [text('index_list_id'), hlink(text('index_list_passphrase'), 'passphrase'), 
                             text('index_list_created'), text('index_list_updated'), 
                             text('index_list_size'), text('index_list_label'), 
                             text('index_list_action') ], 100, undef, $colalign);

    foreach my $hbr (@hbrs) {
        my $id = $hbr->[0];
        my $skpp = lc $hbr->[1];
        print ui_columns_row([@$hbr, 
                                ui_submit(text('index_list_action_restore'),
                                          join(':', 'restore', $id, $skpp)) .
                                ui_submit(text('index_list_action_options'),
                                          join(':', 'advanced', $id, $skpp))
                                          ], $colalign);
    }

    print ui_columns_end();
}


print ui_form_end();

print ui_tabs_end_tab('mode', 'restore');

ui_print_footer('/', text('index'));
