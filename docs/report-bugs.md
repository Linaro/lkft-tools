# Report bugs upstream

When reporting a bug upstream, search for the patch on https://lore.kernel.org

Find the bad patch, download the mbox `https://lore.kernel.org/linux-scsi/20210724072033.1284840-15-hch@lst.de/raw` and edit mbox file.
- add '>' at the beginning of each line.
- trim the raw file and only save the important bits in the patch.
- add `Reported-by: Linux Kernel Functional Testing <lkft@linaro.org>` or `Reported-by: Your Name <YOUR EMAIL@linaro.org>`

Reply something like:
When building `<ARCH>`'s defconfigf '`defconfig file`' on '`linux-repository`' `tag/branch` we see the following error.

`paste the builderror log` and only the important bits of the log and the make commands, for a reference see [example](https://lore.kernel.org/linux-scsi/20210724072033.1284840-15-hch@lst.de/)

When happy with the reply email file, use `git send-email` see [Reply instructions](https://lore.kernel.org/linux-scsi/20210724072033.1284840-15-hch@lst.de/) how to reply.
