<?php
/**
 * Heartbeat receiver. The studio Pi POSTs (or GETs) here every 60s:
 *
 *   curl -fsS -m10 "https://bluetaperigging.com/api/beat.php?k=SECRET"
 *
 * The secret lives in /home/bluetaperigging/bt_config.php (outside public_html,
 * not in Git). Without that file the endpoint is inert.
 */
$cfg = @include __DIR__ . '/../../bt_config.php';
if (!is_array($cfg) || empty($cfg['key'])) {
    http_response_code(503);
    exit('unconfigured');
}

$k = isset($_GET['k']) ? $_GET['k'] : (isset($_SERVER['HTTP_X_BEAT_KEY']) ? $_SERVER['HTTP_X_BEAT_KEY'] : '');
if (!hash_equals((string) $cfg['key'], (string) $k)) {
    http_response_code(403);
    exit('forbidden');
}

$file = !empty($cfg['file']) ? $cfg['file'] : __DIR__ . '/../../bt_heartbeat.dat';
$ok   = @file_put_contents($file, (string) time());

header('Content-Type: text/plain');
http_response_code($ok === false ? 500 : 200);
echo $ok === false ? 'write-failed' : 'ok';
