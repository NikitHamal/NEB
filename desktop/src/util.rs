//! Small helpers shared across modules.
use std::time::{SystemTime, UNIX_EPOCH};

pub fn now_secs() -> u64 {
    SystemTime::now().duration_since(UNIX_EPOCH).map(|d| d.as_secs()).unwrap_or(0)
}

pub fn fmt_bytes(b: u64) -> String {
    const U: [&str; 4] = ["B", "KB", "MB", "GB"];
    let mut v = b as f64;
    let mut i = 0;
    while v >= 1024.0 && i < U.len() - 1 {
        v /= 1024.0;
        i += 1;
    }
    if i == 0 {
        format!("{b} B")
    } else {
        format!("{v:.1} {}", U[i])
    }
}

pub fn initials(name: &str) -> String {
    let mut out = String::new();
    for w in name.split_whitespace().filter(|w| w.chars().next().is_some_and(|c| c.is_alphanumeric())).take(2) {
        if let Some(c) = w.chars().next() {
            out.extend(c.to_uppercase());
        }
    }
    if out.is_empty() {
        "N".into()
    } else {
        out
    }
}

pub fn truncate(s: &str, n: usize) -> String {
    if s.chars().count() <= n {
        s.to_string()
    } else {
        let mut t: String = s.chars().take(n.saturating_sub(1)).collect();
        t.push('…');
        t
    }
}

/// Day number since the epoch — used to rotate the "featured" subject once a day.
pub fn day_number() -> u64 {
    now_secs() / 86_400
}

/// `1 March 2027` from Unix milliseconds (UTC; civil-from-days, no time-zone data needed).
pub fn fmt_date_ms(ms: i64) -> String {
    const M: [&str; 12] = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
    let z = ms.div_euclid(86_400_000) + 719_468;
    let era = z.div_euclid(146_097);
    let doe = z.rem_euclid(146_097);
    let yoe = (doe - doe / 1460 + doe / 36_524 - doe / 146_096) / 365;
    let doy = doe - (365 * yoe + yoe / 4 - yoe / 100);
    let mp = (5 * doy + 2) / 153;
    let d = doy - (153 * mp + 2) / 5 + 1;
    let m = if mp < 10 { mp + 3 } else { mp - 9 };
    let y = yoe + era * 400 + i64::from(m <= 2);
    format!("{d} {} {y}", M[(m - 1) as usize])
}
