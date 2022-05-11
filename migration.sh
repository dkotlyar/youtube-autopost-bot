#!/bin/bash

while [[ $# -gt 0 ]]; do
  key="$1"

  case $key in
    init)
      TYPE='init'
      shift # past argument
      ;;
    commit)
      TYPE='commit'
      shift # past argument
      ;;
    up)
      TYPE='update'
      shift # past argument
      ;;
    -m|--message)
      MESSAGE="$2"
      shift # past argument
      shift # past value
      ;;
    *)    # unknown option
      shift # past argument
      ;;
  esac
done


if [[ "$TYPE" = 'init' ]]; then
  echo 'init'
  python -c "import sys; sys.path.extend(['./src']); from migration import init; init();"
elif [[ "$TYPE" = 'commit' ]]; then
  echo 'commit'
  echo 'message' $MESSAGE
  python -c "import sys; sys.path.extend(['./src']); from migration import commit; commit(message='$MESSAGE');"
elif [[ "$TYPE" = 'update' ]]; then
  echo 'update!'
  python -c "import sys; sys.path.extend(['./src']); from migration import update; update();"
else
  echo 'Unknown command'
fi
