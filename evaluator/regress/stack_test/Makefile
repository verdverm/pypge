# DO NOT DELETE THE BLANK LINE AFTER THIS!
SRCS = \
		../stack.c \
        test.c

OBJS = $(SRCS:.c=.o)
DEPS = $(SRCS:.c=.d)

CFLAGS = -MMD -ggdb -Wall
# LDFLAGS = -L/usr/lib  -L../levmar-2.6 -llevmar -llapack -lblas -lf2c  -lm
LDFLAGS = /home/tony/gocode/src/github.com/verdverm/go-levmar/levmar-2.6/liblevmar.a -llapack -lblas -lf2c -lm

main: $(OBJS)
		gcc -Wall -ggdb $(OBJS) -o test $(LDFLAGS)

-include $(DEPS)

.PHONY: clean distclean
clean:
		rm -f test *.o *.d ../*.o ../*.d
distclean:
		rm -f *.o *.d ../*.o ../*.d
