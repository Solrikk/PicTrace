{pkgs}: {
  deps = [
    pkgs.libGLU
    pkgs.libGL
    pkgs.xsimd
    pkgs.pkg-config
    pkgs.libxcrypt
    pkgs.sqlite-interactive
  ];
}
