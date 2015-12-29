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

install_appd_modules() {
        DELIMITER = '
        VCAP_SERVICES = $DELIMITER + $VCAP_SERVICES +$DELIMITER
        echo $VCAP_SERVICES
        python $BP_DIR/lib/appdynamics_wrapper.py  $BP_DIR $VCAP_SERVICES

}
