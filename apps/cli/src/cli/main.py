import typer

app = typer.Typer()


@app.command()
def hello(name: str):
    print(f"Hello {name}")


@app.command()
def version():
    print("rag-facile v0.1.0")


if __name__ == "__main__":
    app()
