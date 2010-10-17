#!/usr/bin/perl
require 'tklbam-lib.pl';
ReadParse();

my $error;

redirect('') if $in{'cancel'};

if(defined($in{'passphrase'})) {
    if($in{'passphrase'} ne $in{'passphrase_confirm'}) {
        $error = "Error: Passphrase not confirmed correctly";
    } else {
        if($in{'passphrase'} or $in{'confirm'}) {
            eval {
                set_passphrase($in{'passphrase'});
                cache_expire('list');
                webmin_log('passphrase');
            };
            if($@) {
                my $exception = $@;
                ui_print_header(undef, "Error", "", undef, 0, 0);
                die $exception;
            }
            redirect('');
        } else {
            ui_print_header(undef, "Confirm Passphrase Removal", "", undef, 0, 0);
            print ui_confirmation_form('', "Do you really want to remove the passphrase?", 
                [ [ "passphrase", "" ] ],
                [ [ "confirm", "Remove Passphrase" ],
                  [ "cancel",  "Cancel" ] ], undef
                
                );

            ui_print_footer('/', $text{'index'});
            exit;
        }
    }
}

ui_print_header($error, "Set Passphrase", "", undef, 0, 0);

print ui_form_start(undef, "post");
print ui_table_start("Change Backup Passphrase", undef, 2);
print ui_table_row("New passphrase:", 
                   ui_password("passphrase", undef, 20));
print ui_table_row("New passphrase (again):",
                   ui_password("passphrase_confirm", undef, 20));
print ui_table_row(undef, "(Leave empty to remove passphrase)", 2);
print ui_table_end();
print ui_form_end([[undef, 'Change']]);

ui_print_footer('/', $text{'index'});

