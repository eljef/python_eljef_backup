# ElJef Backup

ElJef Backup is a simple backup program that runs operations as steps. It is
easy to integrate into large scripting systems. It is not meant to run as a
replacement for other backup software.

## Things ElJef Backup Does

* Makes full copy backups of data
* Compresses the finished backup (if requested)
* Can mount SSHFS before backups so data can be copied to remote systems
* Can stop containers before backups via docker-compose or docker directly

## Things ElJef Backup Does Not Do

* Does not encrypt backups
* Does not do incremental backups
* Does not do snapshots
  * This could be implemented as a plug-in for filesystem or LVM snapshots
