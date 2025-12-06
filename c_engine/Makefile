CC = gcc
CFLAGS = -O2 -fPIC -Wall -Iinclude
LDFLAGS = -shared

OBJS = src/properties.o src/reactor_models.o src/util.o

all: libcengine.so

libcengine.so: $(OBJS)
	$(CC) $(LDFLAGS) -o $@ $^

src/%.o: src/%.c include/properties.h
	$(CC) $(CFLAGS) -c $< -o $@

clean:
	rm -f src/*.o libcengine.so

.PHONY: all clean
