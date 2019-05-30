# ci-drop
 

set -x
TMATE_TMPDIR=$(mktemp -d /tmp/tmate-ci-XXX)
# install tmate
curl -L \
 https://github.com/tmate-io/tmate/releases/download/2.2.1/tmate-2.2.1-static-linux-amd64.tar.gz \
 | tar xvfzC - $TMATE_TMPDIR --strip-components 1
export PATH=$TMATE_TMPDIR:$PATH
# setup socket and ssh key
socket=$TMATE_TMPDIR/socket
ssh_key=$TMATE_TMPDIR/id_rsa
ssh-keygen -f $ssh_key -t rsa -N ''
# was ensure how to specify key to tmate
eval $(ssh-agent)
ssh-add $ssh_key
# launch detached tmate
tmate -S $socket \
  new-session \
 -d -x 80 -y 25 \
 -s ci-session \
 -n ci-window \
  /bin/bash --login
# wait until it is ready
tmate -S $socket wait tmate-ready
# display the tmate ssh and web connections strings
tmate -S $socket display -p '#{tmate_ssh} # #{tmate_web}'
# Should probably replace this sleep, with a poll mechanism
sleep 9999
