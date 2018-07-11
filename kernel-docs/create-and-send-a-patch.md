#### What to think about when creating a patches to the linux kernel:

1. Create the patch fix against mainline / or linux-next

2. Creating a good changelog:
 - Describe what the kernel does today
 - Explain why that is wrong, e.g., by listing
   * the compiler output for a new buildwarning
   * the crash dump
   * the test failure
 - Describe what your patch does to improve that situation and why that is
      the best solution

3. Add 'Fixes: ...' just above the Sign-off-by, if needed
 * 'Fixes: ...' should only contain
      'Fixes: <first 12 char of the sha> (“shortlog”)' on a single line.
 * Example: 'Fixes: 6129da73bc7b (“shortlog text”)'

4. Add a 'Link:', if needed
 * 'Link: http...' should be added above the first Signed-off-by if we want
      to point to a bugzilla, if we want to point to a lkml email, use
      lore.kernel.org

5. Run checkpatch.pl and get_maintainer.pl on the patch.

6. Send the patch “to=maintainers (and relevant people if needed) cc=lists”

   Example (change based on your needs):
 ```git send-mail configs (make sure they are right)
    git config --global sendemail.supresscc all
    git format-patch -1
    git send-email --to=some@maintainer --cc=linux-kernel@vger.kernel.org \
      --cc=stable@vger.kernel.org --cc=lkft-triage@lists.linaro.org \
      --cc=someone@someplace ./0001-XXXX.patch
 ```

For more info please read [submitting-patches](https://www.kernel.org/doc/html/v4.17/process/submitting-patches.html) guide from the kernel tree.

