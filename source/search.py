try:
	import os
	import sys
	from numb import Separator
	from colorama import Fore,Back
	from colorama import init
	init(autoreset=True)

	E = '[-]'
	I = '[!]'

	def search_by_ext(path, ext, walk, noroot, viewtype, sizer):
		RESULTS = list()
		FOUND_FILES = list()
		JUST_FILES = list()
		NOROOT_TRACE = True

		for root, dirs, files in os.walk(path):
			# checks if the root has no '$RECYCLE.BIN' then procede
			if '$RECYCLE.BIN' not in root:
				# checks if '--no-root'  is triggered
				if noroot:
					track = 0 ####################
					state = False ####################
					for f in files:
						if len(f.split('.')) == 1:
								JUST_FILES.append(f)
						elif f.split('.')[-1] == ext:
							if NOROOT_TRACE: # this prints '...' once. not in every root like in '--view-type [more | less]'
								if track < 1: ####################
									# this raises an error if the user inserts a value not in 'formater_val'
									sizer_func_error(sizer)
									# else print this
									if noroot:
										print("\n", I, "using --no-root, [--view-type] will be disabled!")
										print(" --- ----- ---------- ------------- ---- -- ---------\n")
									NOROOT_TRACE = False
									state = True ####################
							if sizer:
								size = os.path.getsize(os.path.join(root,f))
								sizer_func(sizer, size, f)
							else:
								print(" ", f)
							RESULTS.append(f)
						if state: ####################
							if track < 1: ####################
								track += 1 ####################
						FOUND_FILES.append(f)
					if not(walk):
						break
				
				# but if '--no-root' is not triggered we go here
				else:	
					# checks if '--view-type' is triggered, if is 'more' we go here
					if viewtype == 'more':
						# this raises an error if the user inserts a value not in 'formater_val'
						sizer_func_error(sizer)
						# else print this
						print("\n Directory:" + "(" + Fore.RED + os.getlogin() + Fore.RESET + ")>", root)
						under_root(root, os.getlogin())
						for f in files:
							if len(f.split('.')) == 1:
								JUST_FILES.append(f)
							elif f.split('.')[-1] == ext:
								if sizer:
									size = os.path.getsize(os.path.join(root,f))
									sizer_func(sizer, size, f)
								else:
									print(" ", f)
								RESULTS.append(f)
							FOUND_FILES.append(f)
						if not(walk):
							break		
					
					# checks if '--view-type' is triggered, if is 'less' we go here
					elif viewtype == 'less':
						track = 0 ####################
						state = False ####################
						for f in files:
							if len(f.split('.')) == 1:
								JUST_FILES.append(f)
							elif f.split('.')[-1] == ext:
								if track < 1: ####################
									# this raises an error if the user inserts a value not in 'formater_val'
									sizer_func_error(sizer)
									# else print this
									print("\n Directory:" + "(" + Fore.RED + os.getlogin() + Fore.RESET + ")>", root)
									under_root(root, os.getlogin())
									state = True ####################
								if sizer:
									size = os.path.getsize(os.path.join(root,f))
									sizer_func(sizer, size, f)
								else:
									print(" ", f)
								RESULTS.append(f)
							if state: ####################
								if track < 1: ####################
									track += 1 ####################
							FOUND_FILES.append(f)
						if not(walk):
							break
		print("\n\t" + Separator(str(len(RESULTS))).sep() + " of " + Separator(str(len(FOUND_FILES))).sep() + " Found!" + " (" + str(len(JUST_FILES)) + ")")

	def under_root(root, username, hard_coded=14):
		root = len(root)
		username = len(os.getlogin())
		print('', '-' * (root+username+hard_coded))

	def sizer_func_error(formater):
		formater_val = [None,8,10,20,30]
		if formater not in formater_val:
			print(I, "choose a valid number: 8(Bytes), 10(Kilobytes), 20(Megabytes), 30(Gigabytes)")
			sys.exit()

	def sizer_func(formater, size, file):
		# [!] 'sizer_func' works with  'sizer_func_error'
		formater_val = [8, 10, 20, 30]	
		if formater == formater_val[0]: # Bytes
			print(f'%{15}s Bytes    %{0}s' %(Separator(size).sep(), file))		
		elif formater == formater_val[1]: # Kilobytes
			size = f'{size / 2**10:00.00f}'
			print(f'%{12}s Kb    %{0}s' %(Separator(size).sep(), file))		
		elif formater == formater_val[2]: # Megabytes
			size = f'{size / 2**20:00.01f}'
			print(f'%{10}s Mb    %{0}s' %(Separator(size).sep(), file))		
		elif formater == formater_val[3]: # Gigabytes
			size = f'{size / 2**30:00.02f}'
			print(f'%{6}s Gb    %{0}s' %(Separator(size).sep(), file))


	if __name__ == "__main__":
		import argparse
		
		parser = argparse.ArgumentParser(
			# prog=sys.argv[0].split('.')[0],
			prog='search',
			formatter_class=argparse.RawDescriptionHelpFormatter,
			allow_abbrev=False,)
		
		parser.add_argument('ext', type=str, help='extension to be searched. if not given will give an error')
		parser.add_argument('--view-type', dest='viewtype', choices=['less', 'more'], type=str, default='less', help='lets you view in LESS or MORE mode. if not given will use the LESS mode')
		parser.add_argument('--path', type=str, default=os.getcwd()+'\\', help='path to walk. if not given uses the current root path')
		parser.add_argument('--walk', action='store_true', default=False, help='if triggered, walks the given root else not')
		parser.add_argument('--no-root', dest='noroot', action='store_true', default=False, help='display files without root')
		parser.add_argument('--sizer', type=int, default=None, help='display files sizes in Bytes, Megabytes and/or Gigabytes')
		parser.add_argument('-V', '--version', action='version', version='1.0')

		args = parser.parse_args()

		ext = args.ext
		viewtype = args.viewtype
		path = os.path.realpath(args.path)
		walk = args.walk
		noroot = args.noroot
		sizer = args.sizer

		if os.path.exists(path):
			if not path.endswith('\\'):
				path = path + '\\'
				search_by_ext(path=path, ext=ext, walk=walk, noroot=noroot, viewtype=viewtype, sizer=sizer)
			else:
				search_by_ext(path=path, ext=ext, walk=walk, noroot=noroot, viewtype=viewtype, sizer=sizer)
		else:
			print(E, 'path not exist --> ', repr(path))

except Exception as e:
	print(e)
except KeyboardInterrupt as e:
	print(e)