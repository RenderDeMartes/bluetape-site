<?php
// Offline e-mail alert, run by a cPanel cron job every ~2 minutes:
//   /usr/local/bin/php /home/bluetaperigging/public_html/api/alert.php >/dev/null 2>&1
// (set the cron minute field to a 2-minute interval in the cPanel UI).
//
// Reads the same heartbeat file as status.php and e-mails ONLY when the state
// flips (up->down and down->up), using a small state file so it never spams.
//
// CLI-only: refuses to run over the web so nobody can trigger mail by hitting
// the URL.
if (PHP_SAPI !== 'cli') {
    http_response_code(403);
    exit("cli only\n");
}

$cfg = @include __DIR__ . '/../../bt_config.php';
if (!is_array($cfg)) {
    fwrite(STDERR, "bt_config.php missing\n");
    exit(1);
}

$file  = !empty($cfg['file']) ? $cfg['file'] : __DIR__ . '/../../bt_heartbeat.dat';
$th    = !empty($cfg['threshold']) ? (int) $cfg['threshold'] : 150;
$to    = !empty($cfg['email']) ? $cfg['email'] : '';
$from  = !empty($cfg['from']) ? $cfg['from'] : 'alertas@bluetaperigging.com';
$state = dirname($file) . '/bt_alert_state';

$last = is_file($file) ? (int) @file_get_contents($file) : 0;
$age  = $last ? time() - $last : PHP_INT_MAX;
$now  = $age <= $th ? 'up' : 'down';
$prev = is_file($state) ? trim(@file_get_contents($state)) : 'up';

if ($now !== $prev && $to) {
    if ($now === 'down') {
        $subject = '[Bluetape] El Pi se cayo';
        $body    = "El Pi de Bluetape dejo de reportar al sitio.\n"
                 . 'Ultimo latido: hace ~' . $age . "s (umbral {$th}s).\n"
                 . 'Hora: ' . date('c') . "\n";
    } else {
        $subject = '[Bluetape] El Pi volvio';
        $body    = "El Pi de Bluetape esta reportando de nuevo.\n"
                 . 'Hora: ' . date('c') . "\n";
    }
    @mail($to, $subject, $body, 'From: ' . $from);
}

@file_put_contents($state, $now);
