import io
    """Base class for all exceptions due to failed :class:`Repository` operations."""
    """Exception raised when HEAD is detached (that is, there is no current branch)."""
        super().__init__('Not on any branch')


class Refs:
    """Accessor for the refs stored in a Git repository.
    Will transparently cache the values of all refs.
    """

    empty_id = '0' * 40
        """Get the :class:`Commit` the given ref points to.

        Throws :exc:`KeyError` if ref does not exist.

        """
        """Write the sha1 of the given :class:`Commit` to the ref.

        The ref may or may not already exist.

        """
        old_sha1 = self._refs.get(ref, self.empty_id)
        """Delete the given ref.

        Throws :exc:`KeyError` if ref does not exist.

        """
    def rename(self, msg, *renames):
        """Rename old, new ref pairs."""
        ref_ops = []
        for old_ref, new_ref in renames:
            sha1 = self.get(old_ref).sha1
            ref_ops.append('create %s %s\n' % (new_ref, sha1))
            ref_ops.append('delete %s %s\n' % (old_ref, sha1))
        (
            self._repository.run(['git', 'update-ref', '-m', msg, '--stdin'])
            .raw_input(''.join(ref_ops))
            .discard_output()
        )
        self.reset_cache()

    def batch_update(self, msg, create=(), update=(), delete=()):
        """Batch update/create/delete refs."""
        self._ensure_refs_cache()
        ref_ops = []
        for ref, commit in create:
            ref_ops.append('create %s %s\n' % (ref, commit.sha1))
        for ref, commit in update:
            old_sha1 = self._refs[ref]
            ref_ops.append('update %s %s %s\n' % (ref, commit.sha1, old_sha1))
        for ref in delete:
            old_sha1 = self._refs[ref]
            ref_ops.append('delete %s %s\n' % (ref, old_sha1))
        if ref_ops:
            (
                self._repository.run(['git', 'update-ref', '-m', msg, '--stdin'])
                .raw_input(''.join(ref_ops))
                .discard_output()
            )
            self.reset_cache()

class CatFileProcess:
        fd = p.stdout.fileno()

        # Read until we have the entire header line.
        parts = [os.read(fd, io.DEFAULT_BUFFER_SIZE)]
        while b'\n' not in parts[-1]:
            parts.append(os.read(fd, io.DEFAULT_BUFFER_SIZE))
        out_bytes = b''.join(parts)

        header_bytes, content_part = out_bytes.split(b'\n', 1)
        header = header_bytes.decode('utf-8')
        name, content_type, size = header.split()
        # Read until we have the entire object plus the trailing newline.
        content_len = len(content_part)
        content_parts = [content_part]
        while content_len < size + 1:
            content_part = os.read(fd, io.DEFAULT_BUFFER_SIZE)
            content_parts.append(content_part)
            content_len += len(content_part)
        content = b''.join(content_parts)[:size]

        return content_type, content
class DiffTreeProcesses:

        parts = [os.read(p.stdout.fileno(), io.DEFAULT_BUFFER_SIZE)]
        while not (parts[-1].endswith(b'\n' + end) or parts[-1].endswith(b'\0' + end)):
            parts.append(os.read(p.stdout.fileno(), io.DEFAULT_BUFFER_SIZE))

        data = b''.join(parts)

class Repository:
    """Represents a Git repository."""
        """An :class:`Index` representing the default index file for the repository."""
        """Return an :class:`Index` representing a new temporary index file."""
        """A :class:`Worktree` representing the default work tree."""
        """:class:`IndexAndWorktree` for repository's default index and work tree."""
            sha1 = (
        else:
            return self.get_object(object_type, sha1)
    def get_object(self, object_type, sha1):
        }[object_type](sha1)
        """Return a list of merge bases of two commits."""
        """Apply patch to given tree.

        Given a :class:`Tree` and a patch, either returns the new :class:`Tree`
        resulting from successful application of the patch, or None if the patch
        could not be applied.

        """
        """Return list of submodule paths for the given :class:`Tree`."""
        """Produce patch (diff) between two trees.

        Given two :class:`Tree`s ``t1`` and ``t2``, return the patch that takes
        ``t1`` to ``t2``.
        """
        """Iterate files that differ between two trees.

        Given two :class:`Tree`s ``t1`` and ``t2``, iterate over all files that differ
        between the two trees.

        For each differing file, yield a tuple with the old file mode, the new file
        mode, the old blob, the new blob, the status, the old filename, and the new
        filename.

        Except in case of a copy or a rename, the old and new filenames are identical.

        """
        """Copy Git notes from the old object to the new one."""