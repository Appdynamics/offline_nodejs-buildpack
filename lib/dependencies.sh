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
        DELIMITER="'"
        VCAP_SERVICES="$VCAP_SERVICES"
        echo $VCAP_SERVICES
        LEN=$(echo ${#VCAP_SERVICES})
        if [ LEN -lt 2 ]; then
                echo "doesn't have at least 2 characters"
        else
                python $BP_DIR/lib/appdynamics_wrapper.py  $BP_DIR $VCAP_SERVICES
        fi
        #if [ ! -z $VCAP_SERVICES ]; then
        #  python $BP_DIR/lib/appdynamics_wrapper.py  $BP_DIR '{"appdynamics":[{"name":"node_js","label":"appdynamics","tags":["appdynamics","apm","mobile real-user monitoring","browser real-user monitoring","database monitoring","server monitoring","application analytics"],"plan":"Gold","credentials":{"account-name":"customer1","port":"8090","account-access-key":"e47c0e60-6e7d-41ad-8c64-0ae0d2f6708b","host-name":"52.33.129.11","ssl-enabled":"false"}}]}'
        #fi
}
