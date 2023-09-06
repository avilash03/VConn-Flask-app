from flask import Flask, render_template, request, redirect, url_for
from info import vector_search

application = Flask(__name__)

@application.route("/", methods=["GET", "POST"])
def search():
    if request.method == "POST":
        input_text = request.form["query"]
        threshold = 0.9  # Set your desired similarity threshold here
        top_n = 10  # Number of top results to display

        results = vector_search(input_text, threshold, top_n)

        formatted_results = []

        for content, similarity in results:
            # Split the content into individual parts using "|"
            content_parts = content.split("|")

            formatted_results.append(content_parts)

        return render_template("index.html", query=input_text, results=formatted_results)

    return render_template("index.html")

if __name__ == "__main__":
   application.run()
