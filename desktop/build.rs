// Embeds the NEBians icon + version metadata into the Windows .exe (no-op elsewhere).
fn main() {
    #[cfg(windows)]
    {
        let mut res = winresource::WindowsResource::new();
        res.set_icon("assets/nebians.ico");
        res.set("ProductName", "NEBians");
        res.set("FileDescription", "NEBians Desktop");
        res.set("CompanyName", "NEBians");
        let _ = res.compile();
    }
    println!("cargo:rerun-if-changed=build.rs");
}
