import os
import subprocess
import sys
import textwrap
import threading
from typing import Dict

BOOTSTRAP_TEMPLATE_WIN32 = textwrap.dedent("""
    import sys, io, contextlib, ast
    import matplotlib
    matplotlib.use("Agg")

    import matplotlib.pyplot as plt
    import uuid
    import os
    import time
    import threading

    PLOT_DIR = f"{os.getcwd()}/<OUTPUT_DIR>"
    os.makedirs(PLOT_DIR, exist_ok=True)

    def _sandbox_show():
        epoch = time.time()
        safe_title = ""
        if plt.title:
            title = plt.gca().get_title()
            safe_title = title.replace(" ", "_").replace("/", "_")
        if not safe_title:
            safe_title = "plot"
        fname = f"{epoch}_{safe_title}.png"
        file_path = os.path.join(PLOT_DIR, fname)
        plt.savefig(file_path)
        plt.close()
        print(f"PNG output: {fname}")

    plt.show = _sandbox_show

    _original_savefig = plt.savefig

    def _sandbox_savefig(fname=None, *args, **kwargs):
        if fname is None:
            return _sandbox_show()
        base = os.path.basename(fname)
        epoch = time.time()
        second = str(epoch).split(".")[0].strip()
        if base.startswith(second):
            new_name = base
        else:
            new_name = f"{epoch}_{base}"
        file_path = os.path.join(PLOT_DIR, new_name)
        _original_savefig(file_path, *args, **kwargs)
        print(f"PNG output: {new_name}")

    plt.savefig = _sandbox_savefig

    ns = {}
    ns.setdefault("__name__", "__main__")
    TIMEOUT_SECONDS = <TIMEOUT>

    def read_block():
        lines = []
        for line in sys.stdin:
            if line.rstrip("\\n") == "__END__":
                break
            lines.append(line)
        return "".join(lines)

    class TimeoutFlag(Exception):
        pass

    timeout_triggered = False

    def watchdog():
        global timeout_triggered
        time.sleep(TIMEOUT_SECONDS)
        timeout_triggered = True

    while True:
        header = sys.stdin.readline()
        if not header:
            break
        if header.rstrip("\\n") != "__RUN__":
            continue

        code = read_block()

        buf_out = io.StringIO()
        buf_err = io.StringIO()

        result_value = None
        exception_obj = None

        try:
            tree = ast.parse(code)

            timeout_triggered = False
            t = threading.Thread(target=watchdog, daemon=True)
            t.start()

            with contextlib.redirect_stdout(buf_out), contextlib.redirect_stderr(buf_err):

                if timeout_triggered:
                    raise TimeoutError("Execution timed out")

                if len(tree.body) > 0 and isinstance(tree.body[-1], ast.Expr):
                    exec_code = ast.Module(body=tree.body[:-1], type_ignores=[])
                    exec(compile(exec_code, "<sandbox>", "exec"), ns)

                    if timeout_triggered:
                        raise TimeoutError("Execution timed out")

                    last_expr = ast.Expression(tree.body[-1].value)
                    result_value = eval(compile(last_expr, "<sandbox>", "eval"), ns)
                else:
                    exec(code, ns)

                if timeout_triggered:
                    raise TimeoutError("Execution timed out")

        except BaseException as e:
            exception_obj = repr(e)
            import traceback
            traceback.print_exc(file=buf_err)

        out = buf_out.getvalue()
        err = buf_err.getvalue()

        sys.stdout.write("__OUT__\\n")
        sys.stdout.write(out)
        sys.stdout.write("__END_OUT__\\n")

        sys.stdout.write("__ERR__\\n")
        sys.stdout.write(err)
        sys.stdout.write("__END_ERR__\\n")

        sys.stdout.write("__RESULT__\\n")
        sys.stdout.write(repr(result_value))
        sys.stdout.write("\\n__END_RESULT__\\n")

        sys.stdout.write("__EXC__\\n")
        sys.stdout.write(repr(exception_obj))
        sys.stdout.write("\\n__END_EXC__\\n")

        sys.stdout.flush()
""")

BOOTSTRAP_TEMPLATE_MACOS = textwrap.dedent("""
    import sys, io, contextlib, ast, signal
    import matplotlib
    matplotlib.use("Agg")  # headless backend

    import matplotlib.pyplot as plt
    import uuid
    import os
    import time

    PLOT_DIR = f"{os.getcwd()}/<OUTPUT_DIR>"
    os.makedirs(PLOT_DIR, exist_ok=True)

    def _sandbox_show():
        epoch = time.time()
        safe_title = ""
        if plt.title:
            title = plt.gca().get_title()
            safe_title = title.replace(" ", "_").replace("/", "_")
        if not safe_title:
            safe_title = "plot"
        fname = f"{epoch}_{safe_title}.png"
        file_path = os.path.join(PLOT_DIR, fname)
        plt.savefig(file_path)
        plt.close()
        print(f"PNG output: {fname}")

    plt.show = _sandbox_show

    def _sandbox_savefig(fname=None, *args, **kwargs):
        if fname is None:
            return _sandbox_show()
        base = os.path.basename(fname)
        epoch = time.time()
        second = str(epoch).split(".")[0].strip()
        if base.startswith(second):
            new_name = base
        else:
            new_name = f"{epoch}_{base}"
        file_path = os.path.join(PLOT_DIR, new_name)
        _original_savefig(file_path, *args, **kwargs)
        print(f"PNG output: {new_name}")

    _original_savefig = plt.savefig
    plt.savefig = _sandbox_savefig

    ns = {}
    ns.setdefault("__name__", "__main__")
    TIMEOUT_SECONDS = <TIMEOUT>

    def read_block():
        lines = []
        for line in sys.stdin:
            if line.rstrip("\\n") == "__END__":
                break
            lines.append(line)
        return "".join(lines)

    def timeout_handler(signum, frame):
        raise TimeoutError("Execution timed out")

    signal.signal(signal.SIGALRM, timeout_handler)

    while True:
        header = sys.stdin.readline()
        if not header:
            break
        if header.rstrip("\\n") != "__RUN__":
            continue

        code = read_block()

        buf_out = io.StringIO()
        buf_err = io.StringIO()

        result_value = None
        exception_obj = None

        try:
            tree = ast.parse(code)

            signal.alarm(TIMEOUT_SECONDS)

            with contextlib.redirect_stdout(buf_out), contextlib.redirect_stderr(buf_err):
                if len(tree.body) > 0 and isinstance(tree.body[-1], ast.Expr):
                    exec_code = ast.Module(body=tree.body[:-1], type_ignores=[])
                    exec(compile(exec_code, "<sandbox>", "exec"), ns)

                    last_expr = ast.Expression(tree.body[-1].value)
                    result_value = eval(compile(last_expr, "<sandbox>", "eval"), ns)
                else:
                    exec(code, ns)

        except BaseException as e:
            exception_obj = repr(e)
            import traceback
            traceback.print_exc(file=buf_err)

        finally:
            signal.alarm(0)

        out = buf_out.getvalue()
        err = buf_err.getvalue()

        sys.stdout.write("__OUT__\\n")
        sys.stdout.write(out)
        sys.stdout.write("__END_OUT__\\n")

        sys.stdout.write("__ERR__\\n")
        sys.stdout.write(err)
        sys.stdout.write("__END_ERR__\\n")

        sys.stdout.write("__RESULT__\\n")
        sys.stdout.write(repr(result_value))
        sys.stdout.write("\\n__END_RESULT__\\n")

        sys.stdout.write("__EXC__\\n")
        sys.stdout.write(repr(exception_obj))
        sys.stdout.write("\\n__END_EXC__\\n")

        sys.stdout.flush()
""")

class PersistentSandbox:
    def __init__(self, timeout: int, runtime: str, output_dir: str):
        if sys.platform == "win32":
            bootstrap = BOOTSTRAP_TEMPLATE_WIN32.replace('<TIMEOUT>', str(timeout)).replace('<OUTPUT_DIR>', output_dir)
        else:
            bootstrap = BOOTSTRAP_TEMPLATE_MACOS.replace('<TIMEOUT>', str(timeout)).replace('<OUTPUT_DIR>', output_dir)

        if sys.platform == "win32":
            python_executable = f"{os.getcwd()}\\{runtime}\\Scripts\\python.exe"
        else:
            python_executable = f"{os.getcwd()}/{runtime}/bin/python"

        self.proc = subprocess.Popen(
            [python_executable, "-u", "-c", bootstrap],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=0,
        )
        print("sandbox started, pid:", self.proc.pid)
        print("sandbox poll immediately:", self.proc.poll())
        if self.proc.poll() is not None:
            err = self.proc.stderr.read()
            print("sandbox stderr on startup:\n", err)
        self._lock = threading.Lock()

    def run(self, code: str):
        if self.proc.poll() is not None:
            err = self.proc.stderr.read()
            raise RuntimeError(f"Sandbox worker has exited. Stderr:\n{err}")

        with self._lock:
            self.proc.stdin.write("__RUN__\n")
            self.proc.stdin.write(code)
            if not code.endswith("\n"):
                self.proc.stdin.write("\n")
            self.proc.stdin.write("__END__\n")
            self.proc.stdin.flush()

            stdout_chunks = []
            stderr_chunks = []
            result_value = None
            exception_obj = None

            mode = None
            filen_names = set()

            while True:
                line = self.proc.stdout.readline()
                if not line:
                    raise RuntimeError("Sandbox worker terminated unexpectedly")

                tag = line.rstrip("\n")

                if tag == "__OUT__":
                    mode = "out"; continue
                if tag == "__END_OUT__":
                    mode = None; continue

                if tag == "__ERR__":
                    mode = "err"; continue
                if tag == "__END_ERR__":
                    mode = None; continue

                if tag == "__RESULT__":
                    mode = "result"; continue
                if tag == "__END_RESULT__":
                    mode = None; continue

                if tag == "__EXC__":
                    mode = "exc"; continue
                if tag == "__END_EXC__":
                    mode = None; break

                if mode == "out":
                    if line.startswith("PNG output: "):
                        name = line.split(":")[1].strip()
                        filen_names.add(name)
                    else:
                        stdout_chunks.append(line)
                elif mode == "err":
                    stderr_chunks.append(line)
                elif mode == "result":
                    result_value = line.rstrip("\n")
                elif mode == "exc":
                    exception_obj = line.rstrip("\n")
            if len(filen_names) > 0:
                file_list = ','.join(filen_names)
                stdout_chunks.append(f"Created png file: {file_list}")                

            return {
                "stdout": "".join(stdout_chunks),
                "stderr": "".join(stderr_chunks),
                "result": result_value,
                "exception": exception_obj,
            }

    def close(self):
        try:
            self.proc.stdin.close()
        except Exception:
            pass
        try:
            self.proc.terminate()
        except Exception:
            pass
