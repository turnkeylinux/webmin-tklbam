use strict;
use warnings;
use Test::More;
use File::Temp qw(tempdir);
use File::Copy qw(copy);
use Cwd qw(abs_path);

my $source = abs_path('tklbam');
my $dir = tempdir(CLEANUP => 1);
copy("$source/$_", "$dir/$_") or die $! for qw(init.cgi connect.cgi do_init.cgi);
open my $stub, '>', "$dir/tklbam-lib.pl" or die $!;
print $stub <<'STUB';
use JSON::PP;
sub ReadParse { %main::in = (action => ($ENV{ACTION} || ''), code => ($ENV{CODE} || ''), apikey => ($ENV{APIKEY} || '')); }
sub is_initialized { 0 }
sub has_command { $ENV{LEGACY} ? 0 : 1 }
sub hub_command { die "<network error>\n" if $ENV{FAIL}; return decode_json($ENV{RESULT} || '{}') }
sub tklbam_init { die "<setup error>\n" if $ENV{FAIL}; print "INITIALIZED:@_\n" }
sub redirect { print "REDIRECT:@_\n"; exit }
sub webmin_log { }
sub text { return $_[0] }
sub html_escape { my $s = shift; $s =~ s/&/&amp;/g; $s =~ s/</&lt;/g; $s =~ s/>/&gt;/g; return $s }
sub ui_print_header { }
sub ui_print_footer { }
sub ui_subheading { "HEADING:$_[0] " }
sub ui_form_start { "FORM:$_[0]:$_[1] " }
sub ui_form_end { 'END ' }
sub ui_submit { "BUTTON:$_[0] " }
sub ui_hidden { "HIDDEN:$_[0]:$_[1] " }
sub ui_textbox { 'INPUT ' }
1;
STUB
close $stub;
sub page {
    my ($script, %env) = @_;
    local %ENV = (%ENV, RESULT => '{}', ACTION => '', LEGACY => '', FAIL => '', APIKEY => '', CODE => '', %env);
    open my $run, '-|', $^X, "-I$dir", "$dir/$script" or die $!;
    local $/; my $out = <$run>;
    close $run or die "CGI failed: $script";
    return $out;
}
like(page('init.cgi', RESULT => '{"connection_status":"disconnected"}'), qr/BUTTON:init_connect_button/, 'disconnected server can start connecting');
like(page('init.cgi', RESULT => '{"connection_status":"linked"}'), qr/BUTTON:init_button/, 'linked server can initialize');
like(page('init.cgi', LEGACY => 1), qr/init_legacy_key.*INPUT/, 'older installation retains legacy form');
like(page('connect.cgi', ACTION => 'start', RESULT => '{"user_code":"ABCD-EFGH"}'), qr/ABCD-EFGH.*BUTTON:init_check_button/, 'approval code and check action shown');
like(page('connect.cgi', ACTION => 'poll', CODE => 'ABCD-EFGH', RESULT => '{"status":"pending"}'), qr/init_pending.*ABCD-EFGH.*BUTTON:init_check_button/, 'pending approval can be checked again');
like(page('connect.cgi', ACTION => 'poll', RESULT => '{"connection_status":"linked"}'), qr/REDIRECT:init.cgi/, 'approval returns to setup');
like(page('connect.cgi', ACTION => 'poll', RESULT => '{"status":"expired"}'), qr/init_expired.*init_back/, 'expired connection can be restarted');
like(page('do_init.cgi', FAIL => 1), qr/&lt;setup error&gt;.*init_error_button/s, 'initialization errors are escaped and recoverable');
like(page('do_init.cgi'), qr/INITIALIZED:\s*REDIRECT:/, 'current initialization uses no API key');
like(page('do_init.cgi', LEGACY => 1, APIKEY => 'ABCD2345'), qr/INITIALIZED:ABCD2345/, 'legacy initialization passes valid key');
unlike(page('do_init.cgi', LEGACY => 1, APIKEY => 'A;id'), qr/INITIALIZED:/, 'legacy initialization rejects shell input');
done_testing();
