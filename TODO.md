* Support keeping a defined number of backups
  * Remove backups passed the defined number, oldest first
* Handle docker-compose operations
* Move compress operations to a plugin and run in projects
* Allow plugins to run operations as different users
  * Only if base backup was run as root
  * Useful for attaching to cron jobs
