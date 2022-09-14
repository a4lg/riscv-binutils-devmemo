#! /bin/sh
test $# -eq 2 || exit 1
FILENAME="$1"
HASH_EXPECTED="$2"
test -f "$FILENAME" || exit 1
HASH_VALUE=$(sha256sum "$FILENAME" | awk '{print $1}')
if test "$HASH_VALUE" != "$HASH_EXPECTED"
then
    rm -f "$FILENAME"
    echo "ERROR: downloaded file \`$FILENAME' has invalid hash value." 1>&2
    echo "    expected : $HASH_EXPECTED" 1>&2
    echo "    actual   : $HASH_VALUE"    1>&2
    exit 1
fi
exit 0
