<?php
/**
 * SAMPLE ONLY — do not put the real secret in Git (this repo is public).
 *
 * One-time setup: copy this to  /home/bluetaperigging/bt_config.php
 * (one level ABOVE public_html) via cPanel File Manager, then paste the real
 * key. beat.php / status.php load it from there; it never ships in Git and a
 * deploy never touches it.
 */
return [
    'key'       => 'REPLACE_WITH_SECRET',          // same value the Pi sends as ?k=
    'file'      => __DIR__ . '/bt_heartbeat.dat',  // last-seen timestamp, outside public_html
    'threshold' => 150,                            // seconds; Pi beats every 60s, 2 misses = offline
    'email'     => 'you@example.com',              // where api/alert.php (cron) sends down/up alerts
    'from'      => 'alertas@bluetaperigging.com',  // From: address (a domain address delivers better)
];
