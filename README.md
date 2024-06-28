# notebooks
Runhouse example notebooks.

### Syncing docs to [run-house/runhouse](https://github.com/run-house/runhouse)

1. Create new or update existing `.ipynb` notebook file, and put it in the proper subdirectory folder.

2. Generate the `.rst` (docs) or `.py` (examples) file used for docs generation using the `convert_nb.py` script.
   The script will automatically put the rst file in the corresponding folder in the runhouse repo, so you will need to
   have [run-house/runhouse](https://github.com/run-house/runhouse) cloned down as well.

   From the notebooks git root:

    ```CLI
    python convert_nb.py \
        --files <path_to_ipynb> \
        --rh-repo <path_to_local_rh_git_folder> \
        --format <rst or python>
    ```

   The `--files` arg can take in multiple file paths, or if left empty, will perform the conversion
   for all notebooks in the repo.

3. Create two PRs:

   - `notebooks` repo: Add and commit the updated `.ipynb` file.
   - `runhouse` repo: Add and commit the generated `.rst` or `.py` file.

   Make sure that any PR changes and updates are synced between the two repos.

**Note:** If you are converting to a `.rst` file you will need to have `pandoc` installed. You can install it with:

```CLI
brew install pandoc
```