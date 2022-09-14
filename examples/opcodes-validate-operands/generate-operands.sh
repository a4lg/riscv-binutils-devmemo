#! /bin/sh
RISCV_OPC="$1"
if test ! -d examples/opcodes-validate-operands
then
    echo "ERROR: \`examples/opcodes-validate-operands' not found." 1>&2
    exit 1
fi
if test -f "$RISCV_OPC/opcodes/riscv-opc.c"
then
    RISCV_OPC="$RISCV_OPC/opcodes/riscv-opc.c"
elif test -f "$RISCV_OPC/riscv-opc.c"
then
    RISCV_OPC="$RISCV_OPC/riscv-opc.c"
else test ! -f "$RISCV_OPC"
then
    echo "ERROR: \`$RISCV_OPC' not found." 1>&2
    exit 1
fi

case "$RISCV_OPC" in
riscv-opc.c | */riscv-opc.c)
    ;;
*)
    echo "WARNING: input file \`$RISCV_OPC' is not \`riscv-opc.c'." 1>&2
    echo "check whether this is valid." 1>&2
    ;;
esac

cat "$RISCV_OPC" \
    | grep '^{"' \
    | sed 's/"[^"]*"//;s/[^"]*"//;s/".*//' \
    | sort | uniq >examples/opcodes-validate-operands/operands.txt
