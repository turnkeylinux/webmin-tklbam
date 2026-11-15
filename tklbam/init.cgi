#!/usr/bin/perl
use strict;
use warnings;
our (%in);
require 'tklbam-lib.pl';
ReadParse();
redirect('') if is_initialized();

my ($status, $failure);
if (has_command('turnkey-hub')) {
    eval { $status = hub_command('status --local'); };
} else {
    $status = { connection_status => 'legacy' };
}
$failure = $@ if $@;
ui_print_header(undef, text('init_title'), "", undef, 0, 1);
print ui_subheading(text('init_setup_title'));
if ($failure) {
    print '<p>' . html_escape($failure) . '</p>';
    print '<p>' . text('init_retry_page') . '</p>';
} elsif (($status->{connection_status} || '') eq 'legacy') {
    print '<p>' . text('init_legacy_desc') . '</p>';
    print ui_form_start('do_init.cgi', 'post');
    print '<label>' . text('init_legacy_key') . ' ' . ui_textbox('apikey', '', 20) . '</label> ';
    print ui_submit(text('init_button'));
    print ui_form_end();
} elsif (($status->{connection_status} || '') ne 'linked') {
    print '<p>' . text('init_connect_desc') . '</p>';
    print ui_form_start('connect.cgi', 'post', undef, 'id="hub-connect-form"');
    print ui_hidden('action', 'start');
    print '<button type="submit" class="btn btn-primary">' . text('init_connect_button') . '</button>';
    print ui_form_end();
    print '<p id="hub-connect-message" role="status" aria-live="polite"></p>';
    print <<'SCRIPT';
<script>
(function () {
    var form = document.getElementById('hub-connect-form');
    var message = document.getElementById('hub-connect-message');
    var working = false;
    form.addEventListener('submit', function (event) {
        event.preventDefault();
        if (working) return;
        var tab = window.open('', '_blank');
        if (!tab) {
            message.textContent = 'Allow pop-ups for Webmin, then try again.';
            return;
        }
        working = true;
        message.textContent = 'Preparing the connection. This may take a moment.';
        tab.document.title = 'Connecting to TurnKey Hub';
        tab.document.body.textContent = 'Preparing your connection. Please wait.';
        fetch(new URL(form.getAttribute('action'), document.baseURI).href, {method: 'POST', body: new URLSearchParams(new FormData(form)), credentials: 'same-origin'})
            .then(function (response) { if (!response.ok) throw new Error('request failed'); return response.text(); })
            .then(function (html) {
                var doc = new DOMParser().parseFromString(html, 'text/html');
                var link = doc.querySelector('a.hub-connect-target');
                var target = link && new URL(link.href);
                if (!target || target.origin !== 'https://hub.turnkeylinux.org' ||
                    target.pathname !== '/connect' || !/^[A-Z0-9]{4}-[A-Z0-9]{4}$/.test(target.searchParams.get('code') || '')) {
                    throw new Error('connection unavailable');
                }
                tab.opener = null;
                tab.location.replace(target.href);
                window.location.assign('connect.cgi?action=display&code=' + encodeURIComponent(target.searchParams.get('code')));
            })
            .catch(function (error) { console.error('Hub connection setup:', error);
                tab.close(); working = false;
                form.querySelectorAll('button, input[type=submit]').forEach(function (button) { button.disabled = false; button.classList.remove('disabled'); });
                message.textContent = 'Could not prepare the connection. Check your network and try again.';
            });
    });
}());
</script>
SCRIPT
} else {
    print '<p>' . text('init_setup_desc') . '</p>';
    print ui_form_start('do_init.cgi', 'post');
    print ui_submit(text('init_button'));
    print ui_form_end();
}
print text('init_about_tklbam');
ui_print_footer('/', text('index'));
