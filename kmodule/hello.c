/*  
 *  hello-1.c - The simplest kernel module.
 */
#include <linux/module.h>	/* Needed by all modules */
#include <linux/kernel.h>	/* Needed for KERN_INFO */
#include <linux/sched.h>
#include <linux/proc_fs.h>
#include <linux/buffer_head.h>

int init_module(void)
{
	struct task_struct *bob = (struct task_struct *)NULL;
	struct proc_inode *fred = (struct proc_inode *) NULL;
	struct dentry *a = (struct dentry *) NULL;
	int per_cpu__bh_lrus = NULL;

	printk(KERN_INFO "-------------------\n");
	printk(KERN_INFO "task_struct list_offset: %d\n", (int)&(bob->tasks));

	printk(KERN_INFO "---\n");	
	printk(KERN_INFO "tasks: %d\n", (int)&(bob->tasks));
	printk(KERN_INFO "tasks.next: %d\n", (int)&(bob->tasks.next));
	printk(KERN_INFO "tasks.prev: %d\n", (int)&(bob->tasks.prev));
	printk(KERN_INFO "pid: %d\n", (int)&(bob->pid));
	printk(KERN_INFO "vfs_inode: %d\n", (int)&(fred->vfs_inode));
	printk(KERN_INFO "dentry.d_subdirs: %d\n", (int)&(a->d_subdirs));
	printk(KERN_INFO "buffer_head size: %d\n", sizeof(struct buffer_head));
	printk(KERN_INFO "address of bh_lrus: %08x\n", (unsigned int)&per_cpu(bh_lrus, 0) - (unsigned int)&(per_cpu__bh_lrus) + 0xc0815b60);

	/* 
	 * A non 0 return means init_module failed; module can't be loaded. 
	 */
	return -1;
}

void cleanup_module(void)
{
	printk(KERN_INFO "Goodbye world 1.\n");
}