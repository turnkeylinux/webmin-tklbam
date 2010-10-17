BUILD = build
CONTENTS = *.cgi *.pl *.info config images lang help

$(BUILD)/tklbam.wbm.gz: clean
	mkdir -p $(BUILD)/tklbam/
	cp -a $(CONTENTS) $(BUILD)/tklbam/
	tar -C $(BUILD)/ -zcf $(BUILD)/tklbam.wbm.gz tklbam/

clean:
	rm -rf $(BUILD)
