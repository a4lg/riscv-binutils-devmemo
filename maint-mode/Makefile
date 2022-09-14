# MODIFY FOR YOUR ENVIRONMENT
PREFIX = /opt/maint-mode

AUTOCONF_VERSION  = 2.69
AUTOCONF_EXTDIR   = autoconf-$(AUTOCONF_VERSION)
AUTOCONF_FILENAME = $(AUTOCONF_EXTDIR).tar.gz
AUTOCONF_URL      = https://ftp.gnu.org/gnu/autoconf/$(AUTOCONF_FILENAME)
AUTOCONF_SHA256   = 954bd69b391edc12d6a4a51a2dd1476543da5c6bbf05a95b59dc0dd6fd4c2969
AUTOMAKE_VERSION  = 1.15.1
AUTOMAKE_EXTDIR   = automake-$(AUTOMAKE_VERSION)
AUTOMAKE_FILENAME = $(AUTOMAKE_EXTDIR).tar.gz
AUTOMAKE_URL      = https://ftp.gnu.org/gnu/automake/$(AUTOMAKE_FILENAME)
AUTOMAKE_SHA256   = 988e32527abe052307d21c8ca000aa238b914df363a617e38f4fb89f5abf6260
LIBTOOL_VERSION   = 1.5.26
LIBTOOL_EXTDIR    = libtool-$(LIBTOOL_VERSION)
LIBTOOL_FILENAME  = $(LIBTOOL_EXTDIR).tar.gz
LIBTOOL_URL       = https://ftp.gnu.org/gnu/libtool/$(LIBTOOL_FILENAME)
LIBTOOL_SHA256    = 1c35ae34fe85aa167bd7ab4bc9f477fe019138e1af62678d952fc43c0b7e2f09
GETTEXT_VERSION   = 0.16.1
GETTEXT_EXTDIR    = gettext-$(GETTEXT_VERSION)
GETTEXT_FILENAME  = $(GETTEXT_EXTDIR).tar.gz
GETTEXT_URL       = https://ftp.gnu.org/gnu/gettext/$(GETTEXT_FILENAME)
GETTEXT_SHA256    = 0bf850d1a079fb5a61f0a47b1a9efd35eb44032255375e1cedb0253bc27b376d
GUILE_VERSION     = 1.8.5
GUILE_EXTDIR      = guile-$(GUILE_VERSION)
GUILE_FILENAME    = $(GUILE_EXTDIR).tar.gz
GUILE_URL         = https://ftp.gnu.org/gnu/guile/$(GUILE_FILENAME)
GUILE_SHA256      = e2f63d2d445ffeb072638eab885b1a629e372d1db711c8afb26a62bc56096289

CONFIG_DEPS = Makefile

all: \
	build/stamp-build-autoconf \
	build/stamp-build-automake \
	build/stamp-build-libtool \
	build/stamp-build-gettext \
	build/stamp-build-guile

downloads/stamp-dir:
	@mkdir -p downloads
	@touch $@

downloads/$(AUTOCONF_FILENAME): downloads/stamp-dir
	@if scripts/check-sha256sum.sh $@ $(AUTOCONF_SHA256); then :; else wget -O $@ $(AUTOCONF_URL); scripts/check-sha256sum.sh $@ $(AUTOCONF_SHA256); fi
downloads/$(AUTOMAKE_FILENAME): downloads/stamp-dir
	@if scripts/check-sha256sum.sh $@ $(AUTOMAKE_SHA256); then :; else wget -O $@ $(AUTOMAKE_URL); scripts/check-sha256sum.sh $@ $(AUTOMAKE_SHA256); fi
downloads/$(LIBTOOL_FILENAME): downloads/stamp-dir
	@if scripts/check-sha256sum.sh $@ $(LIBTOOL_SHA256); then :; else wget -O $@ $(LIBTOOL_URL); scripts/check-sha256sum.sh $@ $(LIBTOOL_SHA256); fi
downloads/$(GETTEXT_FILENAME): downloads/stamp-dir
	@if scripts/check-sha256sum.sh $@ $(GETTEXT_SHA256); then :; else wget -O $@ $(GETTEXT_URL); scripts/check-sha256sum.sh $@ $(GETTEXT_SHA256); fi
downloads/$(GUILE_FILENAME): downloads/stamp-dir
	@if scripts/check-sha256sum.sh $@ $(GUILE_SHA256); then :; else wget -O $@ $(GUILE_URL); scripts/check-sha256sum.sh $@ $(GUILE_SHA256); fi

src/stamp-dir: $(CONFIG_DEPS)
	@-rm -r -f src
	@mkdir -p src
	@touch $@

src/stamp-dir-autoconf: src/stamp-dir downloads/$(AUTOCONF_FILENAME)
	@cd src && tar xzf ../downloads/$(AUTOCONF_FILENAME)
	@touch $@
src/stamp-dir-automake: src/stamp-dir downloads/$(AUTOMAKE_FILENAME)
	@cd src && tar xzf ../downloads/$(AUTOMAKE_FILENAME)
	@touch $@
src/stamp-dir-libtool: src/stamp-dir downloads/$(LIBTOOL_FILENAME)
	@cd src && tar xzf ../downloads/$(LIBTOOL_FILENAME)
	@touch $@
src/stamp-dir-gettext: src/stamp-dir downloads/$(GETTEXT_FILENAME)
	@cd src && tar xzf ../downloads/$(GETTEXT_FILENAME)
	@touch $@
src/stamp-dir-guile: src/stamp-dir downloads/$(GUILE_FILENAME) scripts/patch-guile-$(GUILE_VERSION).sh
	@-rm -r -f src/$(GUILE_EXTDIR)
	@( cd src && tar xzf ../downloads/$(GUILE_FILENAME) && cd $(GUILE_EXTDIR) && ../../scripts/patch-guile-$(GUILE_VERSION).sh ); R=$$?; if test $$R -ne 0; then rm -r -f src/$(GUILE_EXTDIR); fi; exit $$R
	@touch $@

build/stamp-dir: src/stamp-dir
	@-rm -r -f build
	@mkdir -p build
	@touch $@

build/stamp-config-autoconf: build/stamp-dir src/stamp-dir-autoconf $(CONFIG_DEPS)
	mkdir -p build/autoconf
	cd build/autoconf && ../../src/$(AUTOCONF_EXTDIR)/configure --prefix=$(PREFIX)
	@touch $@
build/stamp-config-automake: build/stamp-dir src/stamp-dir-automake $(CONFIG_DEPS)
	mkdir -p build/automake
	cd build/automake && ../../src/$(AUTOMAKE_EXTDIR)/configure --prefix=$(PREFIX)
	@touch $@
build/stamp-config-libtool: build/stamp-dir src/stamp-dir-libtool $(CONFIG_DEPS)
	mkdir -p build/libtool
	cd build/libtool && ../../src/$(LIBTOOL_EXTDIR)/configure --prefix=$(PREFIX)
	@touch $@
build/stamp-config-gettext: build/stamp-dir src/stamp-dir-gettext $(CONFIG_DEPS)
	mkdir -p build/gettext
	cd build/gettext && ../../src/$(GETTEXT_EXTDIR)/configure --prefix=$(PREFIX)
	@touch $@
build/stamp-config-guile: build/stamp-dir src/stamp-dir-guile $(CONFIG_DEPS)
	mkdir -p build/guile
	cd build/guile && ../../src/$(GUILE_EXTDIR)/configure --prefix=$(PREFIX) --disable-error-on-warning
	@touch $@

build/stamp-build-autoconf: build/stamp-config-autoconf
	cd build/autoconf && $(MAKE)
	@touch $@
build/stamp-build-automake: build/stamp-config-automake
	cd build/automake && $(MAKE)
	@touch $@
build/stamp-build-libtool: build/stamp-config-libtool
	cd build/libtool && $(MAKE)
	@touch $@
build/stamp-build-gettext: build/stamp-config-gettext
	cd build/gettext && $(MAKE)
	@touch $@
build/stamp-build-guile: build/stamp-config-guile
	cd build/guile && $(MAKE)
	@touch $@

build/stamp-install: build/stamp-dir
	@touch $@

install-autoconf: build/stamp-install build/stamp-build-autoconf
	cd build/autoconf && flock -x ../stamp-install $(MAKE) install
install-automake: build/stamp-install build/stamp-build-automake
	cd build/automake && flock -x ../stamp-install $(MAKE) install
install-libtool: build/stamp-install build/stamp-build-libtool
	cd build/libtool && flock -x ../stamp-install $(MAKE) install
install-gettext: build/stamp-install build/stamp-build-gettext
	cd build/gettext && flock -x ../stamp-install $(MAKE) install
install-guile: build/stamp-install build/stamp-build-guile
	cd build/guile && flock -x ../stamp-install $(MAKE) install

INSTALL_TARGETS = \
	install-autoconf \
	install-automake \
	install-libtool \
	install-gettext \
	install-guile
install: $(INSTALL_TARGETS)
	echo 'export PATH="$(PREFIX)/bin:$$PATH"' >$(PREFIX)/env

clean:
	-rm -r -f build
distclean:
	-rm -r -f downloads
	-rm -r -f src
	-rm -r -f build

.PHONY: all clean distclean install $(INSTALL_TARGETS)
