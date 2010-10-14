#!/usr/bin/perl
require 'tklbam-lib.pl';
use Data::Dumper;

ReadParse();

@vals = keys %in;
die unless @vals;

my ($op, $id, $skpp) = split(/:/, $vals[0], 3);

validate_cli_args($id);

if($op eq 'advanced') {
    ui_print_header(undef, "Advanced Restore", "", undef, 0, 1);

    $hbr = tklbam_list($id);
    my ($id, $skpp, $created, $updated, $size, $label) = @$hbr;

    print ui_form_start('restore_run.cgi', 'form-data');
    print ui_hidden('id', $id), ui_hidden('skpp', lc($skpp));
    print ui_table_start("Configure Restore -- Backup #$id, $label $size MB", 'width=100%', 4);

    print ui_table_row('Time ago:', ui_textbox('time', '', 40), undef,
    ["align=right"]);
    print ui_table_row(hlink('Escrow key:', 'escrow'),
    ui_upload('upload_escrow', 30), undef,
    ['align=right']);

    print ui_table_row('Skip:', 
    ui_checkbox('skip_packages', 1, 'New packages') . '<br />' .
    ui_checkbox('skip_files', 1, 'Filesystem changes') . '<br />' .
    ui_checkbox('skip_database', 1, 'Database'), undef,
    ["align=right"]
    );

    print ui_table_row('Limits:', ui_textarea('limits', "", 3, 30), undef,
    ["align=right"]);

    print ui_table_end();

    print ui_form_end([[undef, 'Run Restore']]);
} elsif($op eq 'restore') {
    redirect("restore_run.cgi?id=$id&skpp=$skpp");
} else {
    error("Unsupported operation");
}

ui_print_footer('/', $text{'index'});
