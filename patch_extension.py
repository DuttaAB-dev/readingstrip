import re

with open('extension.js', 'r') as f:
    content = f.read()

# Remove getPointerWatcher import
content = re.sub(
    r"import \{ getPointerWatcher \} from [\"']resource:///org/gnome/shell/ui/pointerWatcher.js[\"'];\n",
    r"import GLib from 'gi://GLib';\n",
    content
)

# Update toggleStrip
new_toggle_code = """	// add or remove pointer watcher
	if (this.sMiddle.visible) {
            if (!this.pointerWatch) {
                let interval = this.refresh > 0 ? this.refresh : 16;
                this.pointerWatch = GLib.timeout_add(GLib.PRIORITY_DEFAULT, interval, () => {
                    this.syncStrip();
                    return GLib.SOURCE_CONTINUE;
                });
            }
	} else {
            if (this.pointerWatch) {
	        GLib.Source.remove(this.pointerWatch);
	        this.pointerWatch = null;
            }
	}"""
content = re.sub(
    r"\s*// add or remove pointer watcher\s*if \(this\.sMiddle\.visible\) \{\s*if \(\!this\.pointerWatch\) \{\s*this\.pointerWatcher = getPointerWatcher\(\);\s*this\.pointerWatch = this\.pointerWatcher\.addWatch\(\s*this\.refresh,\s*this\.syncStrip\.bind\(this\)\s*\);\s*\}\s*\} else \{\s*if \(this\.pointerWatch\) \{\s*this\.pointerWatch\.remove\(\);\s*this\.pointerWatch = null;\s*\}\s*\}",
    "\n" + new_toggle_code,
    content
)


# Update disable
new_disable_code = """        if (this.pointerWatch){
	    GLib.Source.remove(this.pointerWatch);
        }
	this.pointerWatch = null;"""
content = re.sub(
    r"\s*if \(this\.pointerWatch\)\{\s*this\.pointerWatch\.remove\(\);\s*\}\s*this\.pointerWatch = null;\s*this\.pointerWatcher = null;",
    "\n" + new_disable_code,
    content
)

# Also remove this.pointerWatcher in enable
content = re.sub(
    r"this\.pointerWatcher = null; \s*\n",
    r"",
    content
)


with open('extension.js', 'w') as f:
    f.write(content)

