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
    @date_default_timezone_set('America/Costa_Rica');
    $when = date('d M Y, H:i') . ' (hora CR)';

    if ($now === 'down') {
        $subject = 'El Pi de Bluetape se cayó';
        $accent  = '#ff5f5f';
        $pill    = 'DESCONECTADO';
        $head    = 'El Pi se cayó';
        $lead    = 'Dejó de reportar al sitio.';
        $detail  = 'Último latido hace ~' . $age . 's (umbral ' . $th . 's).';
    } else {
        $subject = 'El Pi de Bluetape volvió';
        $accent  = '#4ade80';
        $pill    = 'EN LÍNEA';
        $head    = 'El Pi volvió';
        $lead    = 'Está reportando de nuevo.';
        $detail  = 'Todo normal otra vez.';
    }

    $html = '<!doctype html><html><body style="margin:0;padding:0;background:#070b12;">'
      . '<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background:#070b12;padding:28px 16px;">'
      . '<tr><td align="center">'
      . '<table role="presentation" width="440" cellpadding="0" cellspacing="0" style="max-width:440px;width:100%;background:#0d1420;border:1px solid #1b2636;border-radius:14px;overflow:hidden;font-family:-apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif;">'
      // top accent bar
      . '<tr><td style="height:4px;background:' . $accent . ';"></td></tr>'
      // header: wordmark + pill
      . '<tr><td style="padding:22px 26px 6px;">'
        . '<table role="presentation" width="100%"><tr>'
          . '<td style="font-size:13px;font-weight:700;letter-spacing:.22em;text-transform:uppercase;color:#7f8da4;">BLUETAPE</td>'
          . '<td align="right"><span style="display:inline-block;padding:5px 11px;border-radius:999px;background:#131c2a;color:' . $accent . ';font-size:11px;font-weight:700;letter-spacing:.12em;">'
            . '<span style="display:inline-block;width:8px;height:8px;border-radius:50%;background:' . $accent . ';vertical-align:middle;margin-right:6px;"></span>' . $pill . '</span></td>'
        . '</tr></table>'
      . '</td></tr>'
      // headline
      . '<tr><td style="padding:10px 26px 2px;font-size:26px;font-weight:800;color:#e8eef7;letter-spacing:-.02em;">' . $head . '</td></tr>'
      . '<tr><td style="padding:2px 26px 18px;font-size:15px;color:#b7c3d6;line-height:1.5;">' . $lead . '</td></tr>'
      // detail box
      . '<tr><td style="padding:0 26px 24px;">'
        . '<table role="presentation" width="100%" style="background:#0a111c;border:1px solid #1b2636;border-radius:10px;">'
          . '<tr><td style="padding:12px 16px;font-size:13px;color:#8b99b0;line-height:1.7;">'
            . '<span style="color:#56647b;">Detalle:</span> ' . $detail . '<br>'
            . '<span style="color:#56647b;">Cuándo:</span> ' . $when
          . '</td></tr>'
        . '</table>'
      . '</td></tr>'
      // footer
      . '<tr><td style="padding:0 26px 22px;font-size:12px;color:#46536a;border-top:1px solid #141d2b;padding-top:16px;">'
        . 'Monitor automático de bluetaperigging.com · <a href="https://bluetaperigging.com" style="color:#5aa9f0;text-decoration:none;">ver sitio</a>'
      . '</td></tr>'
      . '</table></td></tr></table></body></html>';

    // Plain-text fallback for clients that don't render HTML.
    $text = $head . "\n" . $lead . "\n" . $detail . "\nCuándo: " . $when . "\n";

    $boundary = 'bt' . md5(uniqid('', true));
    $headers  = 'MIME-Version: 1.0' . "\r\n"
              . 'From: ' . $from . "\r\n"
              . 'Content-Type: multipart/alternative; boundary="' . $boundary . '"' . "\r\n";
    $msgbody  = '--' . $boundary . "\r\n"
              . 'Content-Type: text/plain; charset=UTF-8' . "\r\n\r\n" . $text . "\r\n"
              . '--' . $boundary . "\r\n"
              . 'Content-Type: text/html; charset=UTF-8' . "\r\n\r\n" . $html . "\r\n"
              . '--' . $boundary . '--';

    // UTF-8 subject so the accents render in every client.
    $encsubject = '=?UTF-8?B?' . base64_encode($subject) . '?=';

    @mail($to, $encsubject, $msgbody, $headers);
}

@file_put_contents($state, $now);
