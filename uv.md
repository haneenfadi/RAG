### Why I used uv instead of venv + pip

I used `uv` as a modern alternative to the traditional `venv` + `pip` workflow. While `venv` only handles environment creation and `pip` installs packages, `uv` combines both into a single tool and provides a more reliable dependency management system. 

The key advantage is that `uv` resolves and locks dependency versions consistently, which prevents conflicts between packages and ensures reproducible environments across development and deployment. In contrast, using `pip` alone can lead to unexpected issues when dependencies change or conflict.

Additionally, `uv` is significantly faster due to its parallelized installation process, making setup and installation much more efficient, especially for projects with many dependencies.

Overall, using `uv` improves reliability, consistency, and performance without requiring changes to the project structure or existing requirements files.

You can install it using :
```bash
pip install uv
```