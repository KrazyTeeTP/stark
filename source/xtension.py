try:
	import os
	import sys
	from numb import Separator
	from colorama import Fore
	from colorama import init
	init(autoreset=True)

	# <path> needed. but if not specified, uses the current directory
	# <walk> feature walks the specified directory
	# <stats> feature displays extensions with statistics
	# <only> feature displays only the statistics

	E = '[-]'
	I = '[!]'

	def extensions(path, walk, stats, only):
		RESULTS = list()
		NO_EXT = list()
		ROOTS = list()

		for root, dirs, files in os.walk(path):
			if '$RECYCLE.BIN' not in root:
				ROOTS.append(root)
				for f in files:
					if len(f.split('.')) > 1:
						f = f.split('.')[-1]
						RESULTS.append(f)
					else:
						NO_EXT.append(f)
				if not(walk):
					break

		if not(only):
			print("\n Directory:" + "(" + Fore.RED + os.getlogin() + Fore.RESET + ")>", path)
			under_root(path, os.getlogin())
			print()
			
			print("", f'%{9}s {"Extensions"}' %("#"))
			print("", f'%{9}s {"=========="}' %("="))

			if len(RESULTS) >= 1:
				for ext in sorted(set(RESULTS)):
					print("", f'%{9}s {ext}' %(Separator(RESULTS.count(ext)).sep()))
			else:
				if len(NO_EXT) >= 1:
					print("", f'%{9}s Only File(s) With No Extensions Found!' %(I))
				else:
					print("", f'%{9}s Nothing Was Found!' %(E))
		
		files_with_ext = len(RESULTS)
		files_with_no_ext = len(NO_EXT)
		extensions = len(set(RESULTS))
		roots_walked = len(ROOTS)
		
		if len(str(files_with_ext)) > len(str(files_with_no_ext)):
			view = len(str(files_with_ext))
		else:
			view = len(str(files_with_no_ext))

		if stats or only:
			if stats:
				print('\n')
			print("Files:")
			print("------")
			print("", f'%{view}s With Extensions!' %(Separator(files_with_ext).sep()))
			print("", f'%{view}s No Extensions!' %(Separator(files_with_no_ext).sep()))
			print("\nExtensions:",)
			print("-----------")
			print("", f'%{view}s Extensions Found!' %(Separator(extensions).sep()))
			print("\nRoots:")
			print("------")
			print("", f'%{view}s Roots Walked!' %(Separator(roots_walked).sep()))

	def under_root(root, username, hard_coded=14):
		root = len(root)
		username = len(os.getlogin())
		print('', '-' * (root+username+hard_coded))

	if __name__ == "__main__":
		import argparse
		
		parser = argparse.ArgumentParser(
			# prog=sys.argv[0].split('.')[0],
			prog='xtension',
			formatter_class=argparse.RawDescriptionHelpFormatter,
			allow_abbrev=False,)
		
		parser.add_argument('--path', type=str, default=os.getcwd()+'\\', help='path to walk. if not given uses the current root path')
		parser.add_argument('--walk', action='store_true', default=False, help='if triggered, walks the given root else not')
		parser.add_argument('--stats', action='store_true', default=False, help='show results with statistics')
		parser.add_argument('--only', action='store_true', default=False, help='show only statistics')
		parser.add_argument('-V', '--version', action='version', version='1.0')

		args = parser.parse_args()

		path = os.path.realpath(args.path)
		walk = args.walk
		stats = args.stats
		only = args.only

		if stats and only:
			print(' --stats\n --only\n' + I + ' can\'t use both')
		else:
			if os.path.exists(path):
				if os.path.isdir(path):
					if not path.endswith('\\'):
						path = path + '\\'
						extensions(path=path, walk=walk, stats=stats, only=only)
					else:
						extensions(path=path, walk=walk, stats=stats, only=only)
				else:
					# print("\n[-] FileNotRequiredError: " + repr(path) + "\n[!] RootPathRequired")
					print(E, "file path not required")
			else:
				# print("\n[-] PathNotFoundError:" + repr(path))
				print(E, "path not found")

except Exception as e:
	print(e)
except KeyboardInterrupt as e:
	print(e)