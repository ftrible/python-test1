"""Verify pytorch installation as an executable script.

This file should not import torch at module import time because importing
the package can trigger heavy native initialisation and OOM in constrained
environments. Use the `verify()` function or run the module as a script.
"""

def verify():
	import torch
	x = torch.rand(5, 3)
	print(x)


if __name__ == '__main__':
	verify()