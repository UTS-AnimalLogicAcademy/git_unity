# Requirements
- python 2.7 or higher
- a version of git that supports LFS
- python interpreter and git must be on the $PATH environment variable (%PATH% for Windows)
- git bash (if you're on Windows)


# Installation
1. Copy the contents of repo_root into your git repository
2. Rename gitattributes to .gitattributes, and gitignore to .gitignore
3. Run setup_osx.sh, setup_windows.bat, or setup_linux.sh depending on your OS

To confirm it worked, see if the following file was created in your git repository:
>.git/hooks/pre-commit

And check that it's contents match the following file:
>git_hooks/pre-commit.sh


# Configuration
The gitattributes file provided comes with some common file types that should be tracked as LFS.  Generally, it is a good thing for this file to be pre-populated as possible, otherwise as users commit new file types, they will get merge conflicts as they are both editing the .gitattributes file.  A utility script is provided which can output all file extensions found inside a directory:

>find_extensions.sh

The whitelist provided contains some common source code types, you can extend it to meet your requirements.  The whitelist provided also  assumes that your Unity project has "forced text" for asset serialisation (which is a good idea if you intend to use git with your Unity project).  Be mindful that if you want to work with binary asset serialisation, you will need to remove any Unity file types from the whitelist (eg: unity, prefab, shader etc)

The gitignore file provided comes with some common patterns for Unity projects - extend or edit as you need.