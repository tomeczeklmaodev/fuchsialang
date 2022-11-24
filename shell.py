# This file is a part of fuchsialang (fxx)
# (c) 2022 tomeczeklmaodev
# https://github.com/tomeczeklmaodev/fuchsialang/

import fxxcore

while True:
	userinput = input("fxx ~$ ")
	result, error = fxxcore.run('<stdin>', userinput)

	if error: print(error.as_str())
	else: print(result)