<?php
/**
 * Live status endpoint for the hero dot AND for UptimeRobot.
 *
 *   HTTP 200 + {"online":true}   when the Pi has checked in recently
 *   HTTP 503 + {"online":false}  when the last heartbeat is stale / missing
 *
 * The 503 is deliberate: UptimeRobot (HTTP monitor on this URL) treats any
 * non-2xx as "down" and e-mails. The browser's fetch() reads the JSON either
 * way, so the dot updates regardless of the status code.
 *
 * Config + heartbeat file live OUTSIDE public_html (see bt_config.php), so the
 * shared secret never ships in the public Git repo and a deploy never wipes
 * the last-seen timestamp.
 */
header('Content-Type: application/json');
header('Cache-Control: no-store, max-age=0');

$cfg = @include __DIR__ . '/../../bt_config.php';

// Not set up yet (no bt_config.php): report unknown, HTTP 200. The dot then
// keeps its default pulse instead of flashing red before setup is finished,
// and no monitor is watching this far ahead of go-live anyway.
if (!is_array($cfg)) {
    http_response_code(200);
    echo json_encode(['online' => null, 'configured' => false]);
    exit;
}

$file = !empty($cfg['file']) ? $cfg['file'] : __DIR__ . '/../../bt_heartbeat.dat';
$th   = !empty($cfg['threshold']) ? (int) $cfg['threshold'] : 150;

$last   = is_file($file) ? (int) @file_get_contents($file) : 0;
$age    = $last ? time() - $last : -1;
$online = $last && $age <= $th;

http_response_code($online ? 200 : 503);
echo json_encode(['online' => $online, 'age' => $age, 'threshold' => $th]);
