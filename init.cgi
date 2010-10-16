#!/usr/bin/perl

require 'tklbam-lib.pl';
ReadParse();

redirect('') if is_initialized();

my $init_error = undef;

validate_cli_args($in{'apikey'});

if($in{'apikey'}) {
    eval {
        tklbam_init($in{'apikey'});
        webmin_log('init');
        redirect('');
    };
    if ($@) {
        $init_error = $@;
    }
}

ui_print_header(undef, "$module_info{'desc'}", "", undef, 0, 1);

print ui_form_start(undef);
print ui_table_start("Init", undef, 2);
print ui_table_row("API-KEY", ui_textbox("apikey", $in{'apikey'}, 20));
print ui_table_end();

print ui_form_end([[undef, 'Save']]);

if ($init_error) {
    print ui_subheading("Error");
    print "<pre>$init_error</pre>";
}

ui_print_footer('/', $text{'index'});
