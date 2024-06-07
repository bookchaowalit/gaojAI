from tabulate import tabulate
import time
import os


def embedding_config_logs(func):
    def wrapper(*args, **kwargs):
        response = func(*args, **kwargs)
        log_id = kwargs.get("log_id")
        verbose = kwargs.get("verbose", False)

        if verbose and log_id:
            current_time = time.strftime("%Y-%m-%d", time.localtime())
            llm_request_logs_filename = f"embedding_config_{current_time}_{log_id}.md"
            folder = f"logs/{log_id}/embedding_config"
            if not os.path.exists(folder):
                os.makedirs(folder)
            output_path = os.path.join(folder, llm_request_logs_filename)

            with open(output_path, "a+") as file:
                file.write(f"## {func.__name__}\n\n")

            headers = [name for name, value in kwargs.items()]
            data = [value for name, value in kwargs.items()]

            table = tabulate(
                [data],
                headers=headers,
                tablefmt="html",
            )
            with open(output_path, "a+") as file:
                file.write("\n")
                file.write(table)
                file.write("\n\n")

            table = tabulate(
                [response],
                headers=["response"],
                tablefmt="html",
            )
            with open(output_path, "a+") as file:
                file.write("\n")
                file.write(table)
                file.write("\n\n")
                file.write(f"End of {func.__name__}\n\n")
        return response

    return wrapper


def database_config_logs(func):
    def wrapper(*args, **kwargs):
        response = func(*args, **kwargs)
        log_id = kwargs.get("log_id")
        verbose = kwargs.get("verbose", False)

        if verbose and log_id:
            current_time = time.strftime("%Y-%m-%d", time.localtime())
            llm_request_logs_filename = f"database_config_{current_time}_{log_id}.md"
            folder = f"logs/{log_id}/database_config"
            if not os.path.exists(folder):
                os.makedirs(folder)
            output_path = os.path.join(folder, llm_request_logs_filename)

            with open(output_path, "a+") as file:
                file.write(f"## {func.__name__}\n\n")

            headers = [name for name, value in kwargs.items()]
            data = [value for name, value in kwargs.items()]

            table = tabulate(
                [data],
                headers=headers,
                tablefmt="html",
            )
            with open(output_path, "a+") as file:
                file.write("\n")
                file.write(table)
                file.write("\n\n")

            table = tabulate(
                [response],
                headers=["response"],
                tablefmt="html",
            )
            with open(output_path, "a+") as file:
                file.write("\n")
                file.write(table)
                file.write("\n\n")
                file.write(f"End of {func.__name__}\n\n")
        return response

    return wrapper


def retrieval_filter_logs(func):
    def wrapper(*args, **kwargs):
        response = func(*args, **kwargs)
        log_id = kwargs.get("log_id")
        verbose = kwargs.get("verbose", False)

        if verbose and log_id:
            current_time = time.strftime("%Y-%m-%d", time.localtime())
            llm_request_logs_filename = (
                f"retrieval_filter_logs_{current_time}_{log_id}.md"
            )
            folder = f"logs/{log_id}/retrieval_filter_logs"
            if not os.path.exists(folder):
                os.makedirs(folder)
            output_path = os.path.join(folder, llm_request_logs_filename)

            with open(output_path, "a+") as file:
                file.write(f"## {func.__name__}\n\n")

            headers = [name for name, value in kwargs.items()]
            data = [value for name, value in kwargs.items()]

            table = tabulate(
                [data],
                headers=headers,
                tablefmt="html",
            )
            with open(output_path, "a+") as file:
                file.write("\n")
                file.write(table)
                file.write("\n\n")

            with open(output_path, "a+") as file:
                file.write(f"End of {func.__name__}\n\n")
        return response

    return wrapper


def retrieval_retrieve_logs(func):
    def wrapper(*args, **kwargs):
        response = func(*args, **kwargs)
        log_id = kwargs.get("log_id")
        verbose = kwargs.get("verbose", False)

        # print("retrieval_retrieve_logs::KWARGS:", kwargs)
        # print("retrieval_retrieve_logs::LOG_ID:", log_id)
        # print("retrieval_retrieve_logs::VERBOSE:", verbose)

        if verbose and log_id:
            current_time = time.strftime("%Y-%m-%d", time.localtime())
            llm_request_logs_filename = f"retrieval_request_{current_time}_{log_id}.md"
            folder = f"logs/{log_id}/retrieval_request"
            if not os.path.exists(folder):
                os.makedirs(folder)
            output_path = os.path.join(folder, llm_request_logs_filename)
            with open(output_path, "a+") as file:
                file.write(f"## {func.__name__}\n\n")

            headers = [name for name, value in kwargs.items()]
            data = [value for name, value in kwargs.items()]
            table = tabulate(
                [data],
                headers=headers,
                tablefmt="html",
            )

            new_response = []
            for i in response:
                new_response.append([i.text, i.metadata.get("caption"), i.score])
            table = tabulate(
                new_response,
                headers=["response"],
                tablefmt="html",
            )
            with open(output_path, "a+") as file:
                file.write("\n")
                file.write(table)
                file.write("\n\n")
                file.write(f"End of {func.__name__}\n\n")
        return response

    return wrapper


def llm_request_logs(func):
    def wrapper(*args, **kwargs):
        response = func(*args, **kwargs)
        log_id = kwargs.get("log_id")
        verbose = kwargs.get("verbose", False)

        # print("llm_request_logs::KWARGS:", kwargs)
        # print("llm_request_logs::LOG_ID:", log_id)
        # print("llm_request_logs::VERBOSE:", verbose)

        if verbose and log_id:
            current_time = time.strftime("%Y-%m-%d", time.localtime())
            llm_request_logs_filename = (
                f"{func.__name__}_llm_request_{current_time}_{log_id}.md"
            )
            folder = f"logs/{log_id}/llm_request"
            if not os.path.exists(folder):
                os.makedirs(folder)
            output_path = os.path.join(folder, llm_request_logs_filename)
            with open(output_path, "a+") as file:
                file.write(f"## {func.__name__}\n\n")

            headers = [name for name, value in kwargs.items()]
            data = [value for name, value in kwargs.items()]

            for arg in args:
                if isinstance(arg, dict):
                    data = [[value for value in arg.values()]]
                    headers = list(arg.keys())
                    table = tabulate(
                        data,
                        headers=headers,
                        tablefmt="html",
                    )
                    with open(output_path, "a+") as file:
                        file.write("\n")
                        file.write(table)
                        file.write("\n\n")

            table = tabulate(
                [response],
                headers=["response"],
                tablefmt="html",
            )
            with open(output_path, "a+") as file:
                file.write("\n")
                file.write(table)
                file.write("\n\n")
                file.write(f"End of {func.__name__}\n\n")
        return response

    return wrapper


def agent_request_logs(func):
    def wrapper(*args, **kwargs):
        response = func(*args, **kwargs)
        log_id = kwargs.get("log_id")
        verbose = kwargs.get("verbose", False)

        # print("agent_request_logs::KWARGS:", kwargs)
        # print("agent_request_logs::LOG_ID:", log_id)
        # print("agent_request_logs::VERBOSE:", verbose)

        if verbose and log_id:
            current_time = time.strftime("%Y-%m-%d", time.localtime())
            llm_request_logs_filename = (
                f"{func.__name__}_agent_request_{current_time}_{log_id}.md"
            )
            folder = f"logs/{log_id}/agent_request"
            if not os.path.exists(folder):
                os.makedirs(folder)
            output_path = os.path.join(folder, llm_request_logs_filename)
            with open(output_path, "a+") as file:
                file.write(f"## {func.__name__}\n\n")

            headers = [name for name, value in kwargs.items()]
            data = [value for name, value in kwargs.items()]

            table = tabulate([data], headers=headers, tablefmt="html")
            with open(output_path, "a+") as file:
                file.write("\n")
                file.write(table)
                file.write("\n\n")

            if response:
                if isinstance(response, list):
                    new_response = []
                    new_header = list(response[0].keys())
                    for i in response:
                        new_response.append(list(i.values()))

                    table = tabulate(
                        new_response,
                        headers=new_header,
                        tablefmt="html",
                    )
                    with open(output_path, "a+") as file:
                        file.write("Reponse")
                        file.write("\n")
                        file.write(table)
                        file.write("\n\n")
                        file.write(f"End of {func.__name__}\n\n")
                elif isinstance(response, str):
                    table = tabulate(
                        [[response]],
                        headers=["response"],
                        tablefmt="html",
                    )
                    with open(output_path, "a+") as file:
                        file.write("Reponse")
                        file.write("\n")
                        file.write(table)
                        file.write("\n\n")
                        file.write(f"End of {func.__name__}\n\n")
        return response

    return wrapper
