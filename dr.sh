#!/bin/bash

#@
#@ ==============================================================================
#@ * DR. King Schultz *
#@ The good doctor. Django's helper script that works with .virtualenv,
#@ git, mysql install, and whatnot
#@ assumes: python2.7, compatible virtualenv, and mysql installed.
#@ ==============================================================================
#@

# =============================================================================================================
# CONFIG
# =============================================================================================================

__SCRIPT_NAME="builder"

# =============================================================================================================
# HELPER METHOD
# =============================================================================================================

function log_info()
{
	echo "`date +'%Y.%m.%d %H:%M:%S'` | $__SCRIPT_NAME | INFO  | $1"
}

function log_header()
{
	echo -e "\033[94m`date +'%Y.%m.%d %H:%M:%S'` | $__SCRIPT_NAME | # $1\033[0m"
}

function log_warn()
{
  echo -e "\033[33m`date +'%Y.%m.%d %H:%M:%S'` | $__SCRIPT_NAME | WARN  | $1\033[0m"
}

function log_error()
{
	echo -e "\033[91m`date +'%Y.%m.%d %H:%M:%S'` | $__SCRIPT_NAME | ERROR | $1\033[0m"
}

#% <doc:help>
#@ help
#@   shows this msg
#@
#% </doc:help>
function cmd_help() {
  cmd=$1
  if [ "$cmd" == "" ]; then
          cat $0 | grep "#@" | grep -v "grep"  | cut -d'@' -f2-1000
  else
          strcmd="sed -n '/<doc:$cmd>/,/<\/doc:$cmd>/p' $0"
          eval $strcmd | grep -v "#%" | cut -d'@' -f2-1000
  fi
}

# =============================================================================================================
# CMD DEFINITION
# =============================================================================================================


function __venvcheck() {

	log_header "VirtualEnv check"

  if [ ! -e .virtualenv/bin/activate ]; then
    log_error "directory .virtualenv is not found. To prepare working env and download necessary packages, please run:"
    log_error "./build.sh env "
    exit -1
  else
    log_info "directory .virtualenv is found. checking if virtualenv is activated..."
  fi

  if [ "True" != $(python -c "import sys; print hasattr(sys,'real_prefix')") ]; then
    log_error "virtual env environment is NOT activated, you need to activate it. try:"
    log_error "source .virtualenv/bin/activate"
    exit -1
  else
    log_info "virtual environment is activated!"
  fi

	if [[ $1 == "-d" ]]; then
	  log_info "django project system check"
	  python manage.py check
	  if [ $? != 0 ]; then
	    log_error "Something is screwed up with your Django code, can you check above?"
	    exit -1;
	  fi
	fi
}

function __iferrmsg() {
  if [ $? != 0 ]; then
    log_error $1
    exit $?
  fi
}


#% <doc:>
#@ env
#@   builds the environment for development:
#@    1. prepares the virtual environment in .virtualenv if not yet prepared,
#@    2. find mysql_config if not in path, and adds dir location to $path
#@    3. install python package requirement into virtual env
#@   this command can be called repeatedly.
#@   call this after a fresh git pull to setup env.
#@   //-> need python2.7 installed
#@
#% </doc:>
function cmd_env() {

  log_header "================================ ENV ====================================="

  if [ ! -d .virtualenv ]; then
    log_info "preparing virtual env environment in $PWD/.virtualenv"
    virtualenv --no-site-packages --distribute .virtualenv;
  else
    log_info "virtual env environment is prepared."
  fi

  source .virtualenv/bin/activate

  # check if virtualenv is activated properly
  __venvcheck

  which mysql_config &> /dev/null
  if [ $? != 0 ]; then
    log_warn "unable to find mysql_config in your PATH. locating in OS..."
    mysql_config_path=$(locate -l1 mysql_config | grep mysql_config )
    PATH=$PATH:${mysql_config_path%/*}
    which mysql_config &> /dev/null
    if [ $? != 0 ]; then
      log_error "unable to resolve mysql_config in path. Please ensure that MYSQL is installed and set $PATH manually."
      return -1
    fi
    log_info "... found at: $(which mysql_config). configured into PATH"
  fi
  log_info "Syncing pip package requirement from $PWD/requirements.txt"
  pip install -r requirements.txt;

  log_info "environment preparation is complete. to activate in your own shell, use:"
  log_info "source .virtualenv/bin/activate"
}

#% <doc:>
#@ run <1:hostport>
#@   checks if env is activated, if so:
#@   runs python manage.py, check its result,
#@   if OK, do django migration commands, git status,
#@   and runserver so we can work on our apps.
#@   [params]
#@     <1:hostport> if specified, will use the specified hostname eg. hostname:6666
#@   //-> need virtualenv activation
#@   //-> need a working DB config and settings.py updated
#@
#% </doc:>
function cmd_run() {

	log_header "================================ RUN ====================================="

  __venvcheck -d  # we check if virtualenv is setup

	log_header "test run"
		python manage.py test
		__iferrmsg "Test run detected errors, please fix above. Aborting run."

  log_header "db migration preps"
	  python manage.py makemigrations
	  __iferrmsg "unable to prepare migrations!"
	  python manage.py migrate

  log_header "git status"
  	git status

	cmd_qrun "$1"
}

#% <doc:>
#@ qrun <1:hostport>
#@   quick run ! don't check for safety. Just! run!
#@   [params]
#@     <1:hostport> if specified, will use the specified hostname eg. hostname:6666
#@   //-> don't need nothing. fuck safety!
#@
#% </doc:>
function cmd_qrun()
{
		log_header "runserver"
		hostname="127.0.0.1:8000"
		if [ "$1" != "" ]; then
			log_warn "hostport override provided [ $1 ]"
			hostname="$1";
		else
			log_info "using standard hostport [ $hostname ]"
	  fi
	  python manage.py runserver $hostname --insecure
}


function cmd_shell()
{
	log_header "=============================== SHELL ===================================="

	__venvcheck -d  # we check if virtualenv is setup

	log_header "test run"
		python manage.py test
		__iferrmsg "Test run detected errors, please fix above. Aborting run."

	log_header "db migration preps"
		python manage.py makemigrations
		__iferrmsg "unable to prepare migrations!"
		python manage.py migrate

	log_header "git status"
		git status

	python manage.py shell
}


#% <doc:>
#@ pip <1:flag [-u] >
#@   compare current pip packages against requirements.txt.
#@   [params]
#@      <1:flag> if -u is specified, will update requirements.txt if diff is found
#@   //-> need virtualenv activation
#@
#% </doc:>
function cmd_pip() {

	log_header "================================ PIP ====================================="

  __venvcheck   # we check if virtualenv is setup
  pip freeze > .requirements.now

	log_header "comparing current packages with [requirements.txt]"
	diff -y .requirements.now requirements.txt > .diff.tmp
	if [ $? == 0 ]; then
		log_info "requirements.txt up to date."
		cat requirements.txt
	elif [ "$1" == "-u" ]; then # if -u specified, update requirements.txt
		log_info "[-u] flag specified & diff detected - updating [requirements.txt]:"
		mv .requirements.now requirements.txt
		cat requirements.txt
		log_header "git status"
		git status | grep requirements.txt
	else # else, discard tmp file, back to 0
		cat .diff.tmp
	fi
	rm .requirements.now &> /dev/null
	rm .diff.tmp &> /dev/null
}




# =============================================================================================================
# MAIN BLOCK
# =============================================================================================================

# if no command passed, exit
if [ "" == "$1" ]; then cmd="help"; else cmd="$1"; fi

# if cmd is passed, call it passing in all parameter (up to 12th..)
"cmd_$cmd" "$2" "$3" "$4" "$5" "$6" "$7" "$8" "$9" "${10}" "${11}" "${12}"

# check result, if cmd not found exit & print help
result=$?
if [ $result == 127 ]; then
	log_error "Command not found: $1"
	help
elif [ $result != 0 ]; then
	# if cmd is found, but exit is still nonzero, print help for that command
	cmd_help $1
fi
# whatever the result, return the exit code from the command
exit $result
