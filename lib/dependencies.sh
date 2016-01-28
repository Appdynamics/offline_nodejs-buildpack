install_node_modules() {
  local build_dir=${1:-}

  if [ -e $build_dir/package.json ]; then
    cd $build_dir
    echo "Pruning any extraneous modules"
    npm prune --unsafe-perm --userconfig $build_dir/.npmrc 2>&1
    if [ -e $build_dir/npm-shrinkwrap.json ]; then
      echo "Installing node modules (package.json + shrinkwrap)"
    else
      echo "Installing node modules (package.json)"
    fi
    npm install --unsafe-perm --userconfig $build_dir/.npmrc 2>&1
  else
    echo "Skipping (no package.json)"
  fi
}

rebuild_node_modules() {
  local build_dir=${1:-}

  if [ -e $build_dir/package.json ]; then
    cd $build_dir
    echo "Rebuilding any native modules"
    npm rebuild 2>&1
    if [ -e $build_dir/npm-shrinkwrap.json ]; then
      echo "Installing any new modules (package.json + shrinkwrap)"
    else
      echo "Installing any new modules (package.json)"
    fi
    npm install --unsafe-perm --userconfig $build_dir/.npmrc 2>&1
  else
    echo "Skipping (no package.json)"
  fi
}

BP_DIR=$(cd $(dirname ${0:-}); cd ..; pwd)

get_file_initial() {
  local FILE_NAME=$(python -c 'import json,sys; f = open("package.json","r"); obj = json.load(f);print obj["scripts"]["start"].split()[1]; f.close()')
  echo $FILE_NAME
}

update_server_appd() {
  local build_dir=${1:-}
  LEN=$(echo ${#VCAP_SERVICES})
  if [ $LEN -ge 4 ]; then
    echo "Reading Environment Variables for Appdynamics"
    echo $VCAP_SERVICES > $build_dir/_vcap_services.txt
    echo $VCAP_APPLICATION > $build_dir/_vcap_application.txt
    local INIT_FILE=$(get_file_initial)
    local TEST_DATA=$(python $BP_DIR/extensions/appdynamics/extension_appdy.py $build_dir)
    echo $TEST_DATA
    echo $TEST_DATA | cat - $build_dir/$INIT_FILE >  $build_dir/tmp.js && mv $build_dir/tmp.js $build_dir/$INIT_FILE
  fi
}
