# Testing conflicting depenencies with poetry - Thanks Databricks...

Normally, we cannot install both `pyspark` and `databricks-connect`, because Databricks, in their infinite wisdom,
decided to ship their own pyspark python modules, which happen to cause name collisions with the vanilla pyspark
package.

So the following code would not know whether to import SparkSession from databricks-connect of vanilla pyspark - which
obviously is a problem.

```python
from pyspark.sql import SparkSession
```

So given that we cannot install them at the same time, what about having two exclusive optional dependencies?
Fortunately, in Poetry we can finally specify this after [#9553](https://github.com/python-poetry/poetry/pull/9553) has
been merged. Thanks guys :heart:

So lets get to work. This repo contains the above mentioned two optional exclusive dependencies. Simply installing the
package and running the test entrypoint with `poetry install && databums` yields:

```
Traceback (most recent call last):
  File "/path/to/clone/spark-databums-conflict/.venv/bin/databums", line 6, in <module>
    sys.exit(main())
             ^^^^^^
  File "/path/to/clone/spark-databums-conflict/src/databums/main.py", line 4, in main
    import pyspark
ModuleNotFoundError: No module named 'pyspark'
```

Good :) - Thats what we expected. We can only import pyspark if we either add the `vanilla` (vanilla pyspark) or the
`databums` extra (databricks-connect).

Running `poetry install --extra=vanilla && databums` yields:

```
Hey there, i imported <class 'pyspark.sql.session.SparkSession'> from <module 'pyspark' from '/path/to/clone/spark-databums-conflict/.venv/lib/python3.12/site-packages/pyspark/__init__.py'>
```

Also Good :-)

Running `poetry install --extra=databums && databums` first uninstalls vanilla pyspark. Yes poetry actually seems to
actively uninstall the non-specified extra dependency, AWESOME! Then it attempts to install `databricks-connect`, and
TADA: `Bus error`. Who would have expected something to just work, when using Databricks.

Let me know if it works for you... 
