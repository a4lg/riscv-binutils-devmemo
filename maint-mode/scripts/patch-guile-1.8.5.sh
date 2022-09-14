#! /bin/sh
# This patch makes Guile 1.8.5 compatible with
# libtool 2.2 or later (tested with libtool 2.4.6).
#
# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2022 Tsukasa OI.

set -e

if \
    test '!' -f guile-1.8.pc.in || \
    test '!' -d guile-readline
then
    echo "ERROR: run this script on the Guile 1.8.5 source directory." 1>&2
    exit 1
fi

patch -p1 <<_END
diff -ru a/Makefile.am b/Makefile.am
--- a/Makefile.am	2008-05-04 21:39:47.000000000 +0000
+++ b/Makefile.am	2022-09-13 18:55:30.000000000 +0000
@@ -35,7 +35,7 @@
 
 TESTS = check-guile
 
-ACLOCAL_AMFLAGS = -I guile-config
+ACLOCAL_AMFLAGS = -I m4 -I guile-config
 
 DISTCLEANFILES = check-guile.log
 
diff -ru a/configure.in b/configure.in
--- a/configure.in	2008-05-07 17:51:15.000000000 +0000
+++ b/configure.in	2022-09-13 18:55:30.000000000 +0000
@@ -64,7 +64,6 @@
 
 dnl Some more checks for Win32
 AC_CYGWIN
-AC_LIBTOOL_WIN32_DLL
 
 AC_PROG_INSTALL
 AC_PROG_CC
@@ -79,8 +78,7 @@
 # for per-target cflags in the libguile subdir
 AM_PROG_CC_C_O
 
-AC_LIBTOOL_DLOPEN
-AC_PROG_LIBTOOL
+LT_INIT([dlopen])
 AC_CHECK_LIB([ltdl], [lt_dlinit], ,
   [AC_MSG_ERROR([libltdl not found.  See README.])])
 
diff -ru a/libguile/guile.c b/libguile/guile.c
--- a/libguile/guile.c	2008-04-07 21:30:03.000000000 +0000
+++ b/libguile/guile.c	2022-09-13 18:55:30.000000000 +0000
@@ -68,8 +68,7 @@
 {
 #if !defined (__MINGW32__)
   /* libtool automagically inserts this variable into your executable... */
-  extern const lt_dlsymlist lt_preloaded_symbols[];
-  lt_dlpreload_default (lt_preloaded_symbols);
+  LTDL_SET_PRELOADED_SYMBOLS();
 #endif
   scm_boot_guile (argc, argv, inner_main, 0);
   return 0; /* never reached */
_END

mkdir -p m4
libtoolize && aclocal && automake -a && autoconf && autoheader
cd guile-readline
libtoolize && aclocal && automake -a && autoconf && autoheader

cat 1>&2 <<_END


Patch/preparation for Guile 1.8.5 is finished!
now, configure Guile with --disable-error-on-warning and you can make it!
_END
