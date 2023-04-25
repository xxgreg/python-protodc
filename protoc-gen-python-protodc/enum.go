package main

import "strconv"

func generateEnumClass(out *Output, enum Enum) {

	out.RenderOne("class [enum_py_name](enum.Enum):",
		"[enum_py_name]", enum.PyName,
	)
	for _, f := range enum.Values {
		out.RenderOne("    [val_py_name] = [val_num]",
			"[val_py_name]", f.PyName,
			"[val_num]", strconv.Itoa(f.Num),
		)
	}
	out.Write("")
	out.Write("")
}
