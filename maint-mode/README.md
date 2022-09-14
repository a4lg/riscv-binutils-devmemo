Maintainer Mode Environment Builder for Binutils
=================================================

It builds and installs programs for maintainer mode.


Important Warning (before Building)
------------------------------------

This `Makefile` only supports Linux.

Programs built by this are quite old and cause many problems outside maintainer mode.
Never install the maintainer mode programs to the path you regularly use.
They should be used only when using the maintainer mode is absolutely necessary.

Edit `PREFIX` line in `Makefile` (default: `/opt/maint-mode`) to set installation path.
Using `make install PREFIX=...` is not recommended (when you repeatedly use this).

Until you finish the installation, **never** add `$PREFIX/bin` to `PATH` environment variable otherwise (at least) Guile will be broken.


Prerequisites
--------------

*   GNU-based toolchain (with `autoconf`, `automake`, `gcc` etc...)
*   GNU Libtool version 2.2 or later
*   GNU Coreutils or equivalent (basic UNIX commands plus `sha256sum`)
*   GNU Wget
*   POSIX-compatible commands:
    *   `awk`
    *   `patch`
    *   `tar`
*   util-linux (to use `flock` command)


Installed Programs (for `--enable-maintainer-mode`)
----------------------------------------------------

*   [GNU Autoconf](https://www.gnu.org/software/autoconf/)
    version 2.69
*   [GNU Automake](https://www.gnu.org/software/automake/)
    version 1.15.1
*   [GNU Libtool](https://www.gnu.org/software/libtool/)
    version 1.5.26
*   [gettext](https://www.gnu.org/software/gettext/)
    version 0.16.1


Installed Program (for `--enable-cgen-maint`)
----------------------------------------------

*   [Guile](https://www.gnu.org/software/guile/)
    version 1.8.5  
    (with a patch to make this compatible with Libtool 2.2 or later)


Note on `--enable-cgen-maint`
------------------------------

Put `cgen` under the source directory of `binutils-gdb` before configuring Binutils / GDB.

Note that `cgen` version used to build various CPU files is inconsistent.
So, if `cgen` works for one architecture, it doesn't work on another.

There's more to note.

1.  Many `cgen`-generated files are modified without regenerating with `cgen`.
2.  There are many, many regressions.

In layman's terms, it's hell to maintain `cgen`-based code.
