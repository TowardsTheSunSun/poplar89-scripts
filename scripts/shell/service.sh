#!/bin/sh
# 标准服务启动
service_name="custom_push"
pid_file="/var/run/${service_name}.pid"
log_file="/data/logs/${service_name}.log"
command_path="/data/app/${service_name}"
command="custom_push.sh"
command_arg=""

function start(){
  # if pid file exist then return;
  if [ -f ${pid_file} ]; then
    echo "${service_name} has started"
    return
  fi

  # start ${service_name} and write pid file
  echo "${service_name} starting..."
  cd ${command_path}
  nohup ./${command} ${command_arg} >> ${log_file} 2>&1 &
  echo $! > ${pid_file}
  echo "${service_name} started"
}

function stop(){
  if [ ! -f ${pid_file} ]; then
    echo "${service_name} has stopped"
    return
  fi
  pid=`cat ${pid_file}`
  # pid file does not exist. get pid from ps
  if [ -z ${pid} ]; then
    pid=`ps -ef|grep ${command}|grep -v grep|awk '{print $2}'|head -n1`
  fi

  # pid is not exist
  if [ -z ${pid} ]; then
    echo "${service_name} has stopped"
    return
  fi

  # kill ${pid}
  echo "kill ${service_name}: ${pid}"
  kill ${pid} 2>/dev/null
  rm ${pid_file}
}

function status(){
  if [ -f ${pid_file} ]; then
    echo `ps -ef|grep ${command}|grep -v grep`
    echo "started"
    return
  fi
  echo "stopped"
}

function main(){
  cmd=$1
  case ${cmd} in
    start)
      start
      ;;
    stop)
      stop
      ;;
    status)
      status
      ;;
    *)
      echo "service.sh [start/stop/status]"
      ;;
  esac
}

main $*
