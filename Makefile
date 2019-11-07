NAME = tklbam
TARGET = $(NAME).wbm.gz
CONTENTS = tklbam

$(TARGET): clean
	find $(CONTENTS) -print0 | \
		xargs -0r touch --no-dereference --date="@$${SOURCE_DATE_EPOCH:-$(shell date +%s)}"
	find $(CONTENTS) -print0 | LC_ALL=C sort -z | \
		tar -I 'gzip -9' -cf $(TARGET) --no-recursion --null --files-from=-

clean:
	rm -rf $(TARGET)
