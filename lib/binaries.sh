needs_resolution() {
  local semver=$1
  if ! [[ "$semver" =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
    return 0
  else
    return 1
  fi
}

install_nodejs() {
  local version="$1"
  local dir="$2"

  if needs_resolution "$version"; then
    echo "Resolving node version ${version:-(latest stable)} via semver.io..."
    version=$($BP_DIR/bin/node $BP_DIR/lib/version_resolver.js "$version")
  fi

  echo "Downloading and installing node $version..."
  local download_url="http://s3pository.heroku.com/node/v$version/node-v$version-$os-$cpu.tar.gz"
  curl "`translate_dependency_url $download_url`" --silent --fail -o /tmp/node.tar.gz || (>&2 $BP_DIR/compile-extensions/bin/recommend_dependency $download_url && false)
  echo "Downloaded [`translate_dependency_url $download_url`]"
  tar xzf /tmp/node.tar.gz -C /tmp
  rm -rf $dir/*
  mv /tmp/node-v$version-$os-$cpu/* $dir
  chmod +x $dir/bin/*
}

install_appdynamics_nodejs() {
  local version="$1"
  local dir="$2"

  if needs_resolution "$version"; then
    echo "Resolving node version ${version:-(latest stable)} via semver.io..."
    version=$($BP_DIR/bin/node $BP_DIR/lib/version_resolver.js "$version")
  fi

  echo "Downloading and installing Appdynamics node 4.2.0.0"
  local download_url="https://download.appdynamics.com/onpremise/internal/4.1.5.0/RC/appdynamics-nodejs-64bit-linux-4.2.0.0.tgz"
  wget "`translate_dependency_url $download_url`" --quiet -o /tmp/appd_node.tgz || (>&2 $BP_DIR/compile-extensions/bin/recommend_dependency $download_url && false)
  echo "Downloaded [`translate_dependency_url $download_url`]"
  tar xzf /tmp/*tgz -C /tmp
  rm -rf $dir/*
  mv /tmp/appdynamics/* $dir
  chmod +x $dir/bin/*
}




install_iojs() {
  local version="$1"
  local dir="$2"

  if needs_resolution "$version"; then
    echo "Resolving iojs version ${version:-(latest stable)} via semver.io..."
    version=$(curl --silent --get --data-urlencode "range=${version}" https://semver.herokuapp.com/iojs/resolve)
  fi

  echo "Downloading and installing iojs $version..."
  local download_url="https://iojs.org/dist/v$version/iojs-v$version-$os-$cpu.tar.gz"
  curl "$download_url" --silent --fail -o /tmp/node.tar.gz || (echo "Unable to download iojs $version; does it exist?" && false)
  tar xzf /tmp/node.tar.gz -C /tmp
  mv /tmp/iojs-v$version-$os-$cpu/* $dir
  chmod +x $dir/bin/*
}

install_npm() {
  local version="$1"

  if [ "$version" == "" ]; then
    echo "Using default npm version: `npm --version`"
  else
    if needs_resolution "$version"; then
      echo "Resolving npm version ${version} via semver.io..."
      version=$(curl --silent --get --data-urlencode "range=${version}" https://semver.herokuapp.com/npm/resolve)
    fi
    if [[ `npm --version` == "$version" ]]; then
      echo "npm `npm --version` already installed with node"
    else
      echo "Downloading and installing npm $version (replacing version `npm --version`)..."
      npm install --unsafe-perm --quiet -g npm@$version 2>&1 >/dev/null
    fi
  fi
}
