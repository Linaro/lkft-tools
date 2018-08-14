#### What to think about when backporting patches to LTS kernels:

1. If a mainline commit doesn’t apply cleanly, send a patch that does.
   Otherwise send an email with the sufficient info (like upstream sha
   and order of patches)

2. ‘commit <sha> upstream.’ should be added just after the shortlog in the changelog.
 * example : ‘commit fdb5c4531c1e0e50e609df83f736b6f3a02896e2 upstream.’ 

3. Add a ‘Link:’
 * 'Link: http...' should be added above the first Signed-off-by if we want
   to point to a bugzilla, if we want to point to a lkml email, use
   lore.kernel.org

4. Emails should always go "To: stable@vger.kernel.org, Cc:gregkh" and always
   CC all the people listed in the changelog as well as the maintainers (use
   scripts/get_maintainer.pl).

5. Always mention which versions require the backport
